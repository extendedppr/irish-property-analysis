from irish_property_analysis.utils import (
    is_nan,
    clean_address_for_comparison,
    remove_duplicates,
    write_to_csv,
    read_csv_to_dict,
    convert_date,
)
from irish_property_analysis.constants import PPR_REPLACEMENT_HEADERS


class Sales:
    def __init__(self, *args, **kwargs):
        self._data = kwargs.get("data", [])
        self._hashes = set()

    def __iter__(self):
        return (i for i in self._data)

    def __len__(self):
        return len(self._data)

    def append(self, sale):
        if not sale in self:
            self._data.append(sale)
            self._hashes.add(sale.hash)

    def __contains__(self, sale):
        if sale.hash in self._hashes:
            return True
        return False

    def serialise(self):
        return [d.serialise() for d in self]

    def filter(self, address=None, county=None, partial=True):
        results = []
        lower_county = county.lower() if county else None
        address_for_comparison = clean_address_for_comparison(address)
        if partial:
            for sale in self:
                if all(
                    [
                        (
                            address_for_comparison
                            in clean_address_for_comparison(sale.address)
                            if address
                            else True
                        ),
                        lower_county in sale.county if county else True,
                    ]
                ):
                    results.append(sale)
        else:
            for sale in self:
                if all(
                    [
                        (
                            address_for_comparison
                            == clean_address_for_comparison(sale.address)
                            if address
                            else True
                        ),
                        lower_county == sale.county if county else True,
                    ]
                ):
                    results.append(sale)

        sales_results = Sales()
        for result in results:
            sales_results.append(Sale.parse(result))

        return sales_results

    def save(self, filepath):
        data = self.serialise()
        data_no_duplicates = remove_duplicates(
            data, subset_fields=["date", "address", "price", "county"]
        )
        write_to_csv(filepath, data_no_duplicates)

    @staticmethod
    def load(filepath):
        print("Getting PPR Data")
        sales = Sales()

        for sales_dict in read_csv_to_dict(filepath, headers=PPR_REPLACEMENT_HEADERS):
            sales.append(Sale.parse(sales_dict))

        print("Got PPR Data")
        return sales


class Sale:
    def __init__(self, *args, **kwargs):
        self.date = convert_date(kwargs["date"])
        self.address = kwargs["address"]

        self.county = kwargs["county"].lower()
        self.price = float(kwargs["price"].replace("\x80", "").replace(",", ""))

        self.not_full_market_price = kwargs["not_full_market_price"]
        self.vat_exclusive = kwargs["vat_exclusive"]

        self.description_of_property_size = kwargs["description_of_property_size"]

        self.description_of_property_size = {
            "greater than or equal to 38 sq metres and less than 125 sq metres": ">38sm <125sqm",
            "greater than 125 sq metres": ">125sqm",
            "less than 38 sq metres": "<38sqm",
        }.get(self.description_of_property_size)

        # FIXME: Below is drek. Normalize to clean strings / do better

        self.eircode = None
        if kwargs.get("eircode"):
            self.eircode = (
                kwargs["eircode"]
                .replace("Baile Átha Cliath", "Dublin")
                .replace("Baile ?tha Cliath", "Dublin")
                if not str(kwargs["eircode"]) == "nan"  # gross, necessary?
                else None
            )

        self.description_of_property = (
            kwargs["description_of_property"]
            .replace(
                "Teach/Árasán Cónaithe Atháimhe",
                "Second-Hand Dwelling house /Apartment",
            )
            .replace("Teach/Árasán Cónaithe Nua", "New Dwelling house /")
            .replace("Teach/?ras?n C?naithe Nua", "New Dwelling house /")
        )

        if self.description_of_property not in [
            "Second-Hand Dwelling house /Apartment",
            "New Dwelling house /Apartment",
            "New Dwelling house /",
        ]:
            self.description_of_property = None

        self.description_of_property = {
            "Second-Hand Dwelling house /Apartment": "second_hand",
            "New Dwelling house /Apartment": "new",
            "New Dwelling house /": "new",
        }.get(self.description_of_property)

    @staticmethod
    def parse(data):
        if isinstance(data, Sale):
            return data
        if isinstance(data, dict):
            data.pop(None, None)
        return Sale(**data)

    def serialise(self):
        return {
            "date": self.date,
            "address": self.address,
            "eircode": self.eircode,
            "county": self.county,
            "price": self.price,
            "not_full_market_price": self.not_full_market_price,
            "vat_exclusive": self.vat_exclusive,
            "description_of_property": self.description_of_property,
            "description_of_property_size": self.description_of_property_size,
            "eircode_routing_key": self.eircode_routing_key,
            "eircode_unique_id": self.eircode_unique_id,
        }

    @property
    def eircode_routing_key(self):
        if not is_nan(self.eircode):
            return self.eircode[:3].lower()
        return None

    @property
    def eircode_unique_id(self):
        if not is_nan(self.eircode):
            return self.eircode[3:].lower()
        return None

    @property
    def hash(self):
        return hash((self.date, self.address, self.eircode, self.price))
