from typing import Iterable, List, Optional, Union

from peewee import (
    Model,
    CharField,
    FloatField,
    IntegerField,
    DateTimeField,
    SqliteDatabase,
    fn,
    SQL,
)

from irish_property_analysis.settings import LISTING_DB_LOCATION


class SaleObject(Model):
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
        database = SqliteDatabase(LISTING_DB_LOCATION)

    def save(self, *args, **kwargs):
        self.searchable_address = self.compute_searchable_address()
        return super(SaleObject, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f'ShareListingObject(original_address="{self.original_address}", clean_address="{self.clean_address}", county="{self.county}", lat="{self.lat}", lng="{self.lng}", price="{self.price}", clean_agent="{self.clean_agent}", ber="{self.ber}", eircode_routing_key="{self.eircode_routing_key}", m_squared="{self.m_squared}", constructed_date="{self.constructed_date}", beds="{self.beds}", baths="{self.baths}", property_type="{self.property_type}", published_date="{self.published_date}")'

    def compute_searchable_address(self) -> str:
        return self.original_address.replace(" ", "").replace(",", "").lower()

    def serialise(self):
        return {
            "original_address": self.original_address,
            "clean_address": self.clean_address,
            "county": self.county,
            "lat": self.lat,
            "lng": self.lng,
            "price": self.price,
            "clean_agent": self.clean_agent,
            "ber": self.ber,
            "eircode_routing_key": self.eircode_routing_key,
            "m_squared": self.m_squared,
            "constructed_date": self.constructed_date,
            "beds": self.beds,
            "baths": self.baths,
            "property_type": self.property_type,
            "published_date": self.published_date,
        }


class SaleDB:
    def __init__(self) -> None:
        self.create_connection()

    def __len__(self) -> int:
        return SaleObject.select().count()

    def __iter__(self) -> Iterable[SaleObject]:
        return SaleObject.select().iterator(chunk_size=100)

    def drop_data(self) -> None:
        SaleObject.delete().execute()

    def create_connection(self) -> None:
        db = SqliteDatabase(LISTING_DB_LOCATION)
        db.connect()
        db.create_tables([SaleObject])

    def filter(
        self,
        address_substrs=None,
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
    ) -> List[SaleObject]:
        filters = {
            "county": county if county else None,
            "clean_agent": clean_agent if clean_agent else None,
            "ber": ber if ber else None,
            "eircode_routing_key": eircode_routing_key if eircode_routing_key else None,
            "beds": beds if beds else None,
            "baths": baths if baths else None,
            "property_type": property_type if property_type else None,
        }

        query = SaleObject.select()

        for field, value in filters.items():
            if value is not None:
                field_name = getattr(SaleObject, field)
                if partial:
                    query = query.where(field_name.ilike(f"%{value}%"))
                else:
                    query = query.where(field_name.ilike(value))

        if address:
            address = address.replace(" ", "").replace(",", "").lower()
            if partial:
                query = query.where(SaleObject.searchable_address.contains(address))
            else:
                query = query.where(SaleObject.searchable_address == address)

        if address_substrs:
            for address_substr in address_substrs:
                if partial:
                    query = query.where(
                        SaleObject.searchable_address.contains(address_substr)
                    )
                else:
                    query = query.where(SaleObject.searchable_address == address_substr)

        return [obj for obj in query]


sale_db = SaleDB()
