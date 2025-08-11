from io import BytesIO

import requests
import pandas as pd

from irish_property_analysis.settings import BUS_STOP_DATA_LOCATION


def main():
    url = "https://www.transportforireland.ie/transitData/Data/NaPTAN.xlsx"

    print(f"Downloading: {url}")

    response = requests.get(url)
    response.raise_for_status()

    xls = pd.ExcelFile(BytesIO(response.content))
    for sheet_name in xls.sheet_names:
        if "StopPoints" in sheet_name:
            df = pd.read_excel(xls, sheet_name=sheet_name)
            df.to_csv(BUS_STOP_DATA_LOCATION, index=False)
            print(f"Wrote to: {BUS_STOP_DATA_LOCATION}")


if __name__ == "__main__":
    main()
