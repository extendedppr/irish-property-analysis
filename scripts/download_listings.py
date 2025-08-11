import os
import json

import requests

from irish_property_analysis.settings import LISTINGS_DATA_LOCATION
from irish_property_analysis.constants import LISTINGS_BASE_URL, LISTINGS_DATA_OPTIONS


def main():
    page_size = 10000
    for data_option in LISTINGS_DATA_OPTIONS:
        url = f"{LISTINGS_BASE_URL}?pageSize={page_size}&dataOption={data_option}"
        data = []
        print(f"Fetching data for: {data_option}")
        while url:
            r = requests.get(url).json()
            data.extend(r["data"])
            url = r.get("next")

        output_file = os.path.join(LISTINGS_DATA_LOCATION, f"{data_option}.json")
        with open(output_file, "w") as f:
            json.dump(data, f)

        print(f"Saved {data_option} data to {output_file}")


if __name__ == "__main__":
    main()
