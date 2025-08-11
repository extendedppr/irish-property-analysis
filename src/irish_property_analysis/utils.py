import csv
import os
import ujson
import requests
import zipfile
import shutil
from datetime import datetime
from functools import lru_cache
from math import radians, sin, cos, asin, sqrt, isnan

import numpy as np

from irish_property_analysis.settings import LISTINGS_DATA_LOCATION, BAD_MERGE_ATTRS
from irish_property_analysis.constants import (
    PPR_URL,
    TRICKY_STR_TABLE,
    EARTH_RADIUS
)


def remove_duplicates(data, subset_fields=None):
    """
    If subset_fields is None then all fields will be used to deduplicate.
    """
    seen = set()
    unique_data = []
    for row in data:
        if subset_fields:
            key = tuple(row[field] for field in subset_fields)
        else:
            key = row.values()

        if key not in seen:
            unique_data.append(row)
            seen.add(key)
    return unique_data


def write_to_csv(filepath, data):
    if not data:
        print(f"No data to write to: {filepath}")
        return

    fieldnames = data[0].keys()
    with open(filepath, mode="w", newline="", encoding="ISO-8859-1") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def read_csv_to_dict(filepath, headers=None):
    with open(filepath, mode="r", encoding="ISO-8859-1") as file:
        if headers is not None:
            reader = csv.DictReader(file, fieldnames=headers)
            next(reader)
        else:
            reader = csv.DictReader(file)
        return [row for row in reader]


@lru_cache(maxsize=100)
def clean_address_for_comparison(address):
    address = clean_address(address)

    if not address:
        return

    # TODO: road to rd, street to st etc.

    return address.lower()


def clean_address(address):
    # TODO: in here do a clean_string which is a more basic version of clean_address, not taking into account road->rd etc.

    if not address or not isinstance(address, str):
        return

    return address.translate(TRICKY_STR_TABLE).strip()


def mean_data(data: list, attr: str) -> list:
    for item in data:
        if isinstance(item[attr], list):
            item[attr] = sum(item[attr]) / len(item[attr])
    return data


def print_bad_merges(merged_listing):
    # Handy for debugging
    for k in BAD_MERGE_ATTRS:
        if isinstance(merged_listing[k], list):
            print(k)
            print(merged_listing[k])
            print()


def read_json(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(filepath)

    with open(filepath, "r") as fh:
        return ujson.loads(fh.read())


@lru_cache(maxsize=100)
def convert_date(date_str):
    if isinstance(date_str, datetime):
        return date_str

    if len(date_str) == 10:
        return datetime.strptime(date_str, "%d/%m/%Y")
    if len(date_str) == 19:
        return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    else:
        return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S.%f")


def is_nan(value):
    return value is None or (isinstance(value, (float, int)) and isnan(value))


def is_sale_date_within_range(base_date: str | datetime, cmp_date: str | datetime):
    return abs((convert_date(base_date) - convert_date(cmp_date)).days) < (
        365 / 2
    )  # TODO: to settings


def get_all_historical_listings() -> list:
    print('Getting Historical Listings')
    data = read_json(os.path.join(LISTINGS_DATA_LOCATION, "allHistoricalListings.json"))
    print('Got Historical Listings')
    return data


def get_shares() -> list:
    print('Getting Shares')
    data = read_json(os.path.join(LISTINGS_DATA_LOCATION, "shares.json"))
    for d in data:
        d.pop("beds", None)
    print('Got Shares')
    return data


def get_rentals() -> list:
    print('Getting Rentals')
    data = read_json(os.path.join(LISTINGS_DATA_LOCATION, "rentals.json"))
    print('Got Rentals')
    return data


def download_ppr_zip(filename):
    req = requests.get(PPR_URL, verify=False)
    with open(filename, "wb") as output_file:
        output_file.write(req.content)


def extract_ppr_zip(zip_location, extract_to):
    dirpath = os.path.splitext(zip_location)[0]
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    with zipfile.ZipFile(zip_location, "r") as zip_ref:
        zip_ref.extractall(dirpath)

    shutil.copy(os.path.join(dirpath, "PPR-ALL.csv"), extract_to)


def minimize_str(string, length=50):
    string = str(string).replace("\n", " ")

    while "  " in string:
        string = string.replace("  ", " ")

    return string[: length - 3] + "..." if len(string) > length else string


def none_to_str(string):
    return "" if not string else string


def haversine_vectorized(lat1, lon1, lat2, lon2, radius_km=1):
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = np.sin(dlat / 2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2.0)**2
    c = 2 * np.arcsin(np.sqrt(a))

    return (radius_km * c) * EARTH_RADIUS
