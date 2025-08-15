PPR_URL = "https://www.propertypriceregister.ie/website/npsra/ppr/npsra-ppr.nsf/Downloads/PPR-ALL.zip/$FILE/PPR-ALL.zip"

PPR_REPLACEMENT_HEADERS = [
    "date",
    "address",
    "eircode",
    "county",
    "price",
    "not_full_market_price",
    "vat_exclusive",
    "description_of_property",
    "description_of_property_size",
]

LISTINGS_BASE_URL = "https://e4expolexk.execute-api.eu-west-1.amazonaws.com/api/data/"
LISTINGS_DATA_OPTIONS = {
    "all_shares": "shares",
    "all_rentals": "rentals",
    "all_sales": "allHistoricalListings",
    # NOTE: Below not used yet
    #"ppr_price": "PPRPrice",
    #"matched_with_ppr": "matchedWithPPR",
}

TRICKY_STR_TABLE = str.maketrans(
    {
        "Â": "",
        "Ã": " ",
        "\x82": "",
        "\x83": "",
        "º": "á",
        "¡": "",
        "³": "",
    }
)

EARTH_RADIUS = 6371.0
