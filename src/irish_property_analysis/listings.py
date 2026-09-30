from typing import Iterable

from peewee import (
    Model,
    CharField,
    FloatField,
    IntegerField,
    DateTimeField,
    SqliteDatabase,
)

from irish_property_analysis.settings import LISTING_DB_LOCATION
from irish_property_analysis.utils import haversine_vectorized


LISTING_DB = SqliteDatabase(LISTING_DB_LOCATION)
SERIALIZED_LISTING_FIELDS = (
    "original_address",
    "clean_address",
    "county",
    "lat",
    "lng",
    "price",
    "clean_agent",
    "ber",
    "eircode_routing_key",
    "m_squared",
    "constructed_date",
    "beds",
    "baths",
    "property_type",
    "published_date",
)


def normalize_searchable_address(address: str) -> str:
    return address.replace(" ", "").replace(",", "").lower()


class ListingObject(Model):
    original_address = CharField()
    clean_address = CharField()
    county = CharField(null=True)
    lat = FloatField(null=True)
    lng = FloatField(null=True)
    price = FloatField(null=True)
    clean_agent = CharField(null=True)
    ber = CharField(null=True)
    eircode_routing_key = CharField(null=True)
    m_squared = FloatField(null=True)
    constructed_date = IntegerField(null=True)
    beds = FloatField(null=True)
    baths = FloatField(null=True)
    property_type = CharField(null=True)
    published_date = DateTimeField(null=True, default=None)
    searchable_address = CharField()

    class Meta:
        database = LISTING_DB
        legacy_table_names = True
        legacy_table_naming = True

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.__repr__ = ListingObject._listing_repr

    def save(self, *args, **kwargs):
        self.searchable_address = self.compute_searchable_address()
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self._listing_repr()

    def _listing_repr(self) -> str:
        attrs = ", ".join(
            f'{field}="{self.__data__.get(field)}"'
            for field in SERIALIZED_LISTING_FIELDS
        )
        return f"{self.__class__.__name__}({attrs})"

    def compute_searchable_address(self) -> str:
        return normalize_searchable_address(self.original_address)

    def serialize(self):
        return {field: self.__data__.get(field) for field in SERIALIZED_LISTING_FIELDS}


class ListingDB:
    model_class = ListingObject

    def __init__(self) -> None:
        self.create_connection()

    def __len__(self) -> int:
        return self.model_class.select().count()

    def __iter__(self) -> Iterable[ListingObject]:
        return self.model_class.select().iterator()

    def drop_data(self) -> None:
        self.model_class.delete().execute()

    def create_connection(self) -> None:
        LISTING_DB.connect(reuse_if_open=True)
        LISTING_DB.create_tables([self.model_class])
        self.db = LISTING_DB

    def close(self):
        if not LISTING_DB.is_closed():
            LISTING_DB.close()

    def filter(
        self,
        address_substrs=None,
        exclude_address_substrs=None,
        address=None,
        county=None,
        clean_agent=None,
        ber=None,
        eircode_routing_key=None,
        m_squared=None,
        constructed_date=None,
        beds=None,
        baths=None,
        property_type=None,
        published_date=None,
        partial: bool = False,
        coordinates=None,
        search_radius_km=None,
    ) -> list[ListingObject]:
        filters = {
            "county": county,
            "clean_agent": clean_agent,
            "ber": ber,
            "eircode_routing_key": eircode_routing_key,
            "beds": beds,
            "baths": baths,
            "property_type": property_type,
        }
        query = self.model_class.select()

        for field, value in filters.items():
            if value is not None:
                field_name = getattr(self.model_class, field)
                query = query.where(
                    field_name.ilike(f"%{value}%")
                    if partial
                    else field_name.ilike(value)
                )

        if address:
            searchable_address = normalize_searchable_address(address)
            if partial:
                query = query.where(
                    self.model_class.searchable_address.contains(searchable_address)
                )
            else:
                query = query.where(
                    self.model_class.searchable_address == searchable_address
                )

        for address_substr in address_substrs or []:
            query = query.where(
                self.model_class.searchable_address.contains(address_substr)
            )

        for exclude_address_substr in exclude_address_substrs or []:
            query = query.where(
                ~(self.model_class.searchable_address.contains(exclude_address_substr))
            )

        result = list(query)
        if not coordinates:
            return result

        result = [row for row in result if row.lat and row.lng]
        distances = haversine_vectorized(
            coordinates[0],
            coordinates[1],
            [row.lat for row in result],
            [row.lng for row in result],
        )
        mask = (distances <= search_radius_km).tolist()

        return [row for row, keep in zip(result, mask) if keep]
