from io import BytesIO

import requests
import pandas as pd

from irish_property_analysis.settings import (
    PRIMARY_SCHOOLS_DATA_LOCATION,
    SECONDARY_SCHOOLS_DATA_LOCATION,
)


def main():
    configs = [
        {
            "url": "https://assets.gov.ie/static/documents/Data_on_Individual_Schools_PPOD_2024_25.xlsx",
            "sheet": "School List",
            "data_location": PRIMARY_SCHOOLS_DATA_LOCATION,
        },
        {
            "url": "https://assets.gov.ie/static/documents/Data_on_Individual_Schools_Mainstream_2024_25.xlsx",
            "sheet": "Mainstream Schools",
            "data_location": SECONDARY_SCHOOLS_DATA_LOCATION,
        },
    ]

    for config in configs:
        print(f"Downloading: {config['url']}")

        response = requests.get(config["url"])
        response.raise_for_status()

        xls = pd.ExcelFile(BytesIO(response.content))
        for sheet_name in xls.sheet_names:
            if config["sheet"] == sheet_name:
                df = pd.read_excel(xls, sheet_name=sheet_name)
                df.to_csv(config["data_location"], index=False)
                print(f"Wrote to: {config['data_location']}")


if __name__ == "__main__":
    main()
