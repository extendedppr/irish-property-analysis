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

Run `poetry run download_listings`


## RTB data

Visit [rtb-scraper](https://github.com/extendedppr/) and follow the scraping data steps.


# Searching Properties

Run `poetry run get_property_details --county dublin --address-substr-csv 87,avenue`

```bash
usage: get_property_details [-h] [--address-substr-csv ADDRESS_SUBSTR_CSV] [--county COUNTY] [--all ALL]

Get all available details about an address

options:
  -h, --help            show this help message and exit
  --address-substr-csv ADDRESS_SUBSTR_CSV
                        CSV values of address substrings that must be within the found address (e.g. '13,dublin,grand canal')
  --county COUNTY       County to search in
  --all ALL             Don't truncate long strings
```
