# Irish Property Analysis

A project focused on analyzing, and visualizing data from Ireland’s property market. It combines rental data from the Residential Tenancies Board (RTB) with scraped historical datasets from property platforms for sales, rentals, and shares.

# Demo

This shows the results of `poetry run get_property_details --county dublin --address-substr-csv 87,avenue`

![demo](./assets/demo.gif)

# Installation

```bash
poetry install
```

# Downloading / Scraping Data

## Historical Listing Data

```bash
poetry run download_listings
```

## Supplementary Listing Data

```bash
poetry run download_ppr
poetry run download_school_data
poetry run download_bus_data
```

## PPR data

Visit [ppr](https://github.com/extendedppr/ppr) and follow the scraping data steps.

## RTB data

Visit [rtb-scraper](https://github.com/extendedppr/rtb-scraper) and follow the scraping data steps.


# Searching Properties

Run `poetry run get_property_details --county dublin --address-substr-csv 87,avenue`

```bash
usage: get_property_details [-h] [--address-substr-csv ADDRESS_SUBSTR_CSV] [--county COUNTY]
                            [--school-radius-km SCHOOL_RADIUS_KM]
                            [--bus-stop-radius-km BUS_STOP_RADIUS_KM] [--all]
                            [--exclude-address-substr-csv EXCLUDE_ADDRESS_SUBSTR_CSV]

Get all available details about an address

options:
  -h, --help            show this help message and exit
  --address-substr-csv ADDRESS_SUBSTR_CSV
                        CSV values of address substrings that must be within the found address (e.g.
                        '13,dublin,grand canal')
  --county COUNTY       County to search in
  --school-radius-km SCHOOL_RADIUS_KM
                        How wide around a property to search for schools
  --bus-stop-radius-km BUS_STOP_RADIUS_KM
                        How wide around a property to search for bus stops
  --all                 Don't truncate long strings
  --exclude-address-substr-csv EXCLUDE_ADDRESS_SUBSTR_CSV
                        CSV values of address substrings that must not be within the found address
                        (e.g. '13,dublin,grand canal')
```
