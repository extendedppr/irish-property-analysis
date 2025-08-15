import requests

from irish_property_analysis.constants import LISTINGS_BASE_URL, LISTINGS_DATA_OPTIONS
from irish_property_analysis.utils import chunks
from irish_property_analysis.rentals import rental_db, RentalObject
from irish_property_analysis.shares import share_db, ShareObject
from irish_property_analysis.sales import sale_db, SaleObject


def main():
    page_size = 10000
    for name, data_option in LISTINGS_DATA_OPTIONS.items():
        url = f"{LISTINGS_BASE_URL}?pageSize={page_size}&dataOption={data_option}"
        data = []
        print(f"Fetching data for: {name}")
        while url:
            r = requests.get(url).json()
            data.extend(r["data"])
            url = r.get("next")

        if name in {"all_rentals", "all_sales", "all_shares"}:
            match name:
                case "all_rentals":
                    object_class = RentalObject
                    rental_db.drop_data()
                case "all_sales":
                    object_class = SaleObject
                    sale_db.drop_data()
                case "all_shares":
                    object_class = ShareObject
                    share_db.drop_data()

            insert_data = []
            for obj in data:
                obj.pop("_id")

                obj["lat"] = obj["location"]["coordinates"][1]
                obj["lng"] = obj["location"]["coordinates"][0]
                obj.pop("location")

                obj["searchable_address"] = (
                    obj["original_address"].replace(" ", "").replace(",", "").lower()
                )

                insert_data.append(obj)
            for chunk in chunks(insert_data, 10000):
                object_class.insert_many(chunk).execute()
        else:
            print(f'Not sure how to deal with data of type "{name}"')

        print(f"Saved {data_option}")


if __name__ == "__main__":
    main()
