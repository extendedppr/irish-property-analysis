import os
import sys


TEST_ENV = False
if "pytest" in sys.modules:
    TEST_ENV = True


LISTINGS_DATA_LOCATION = (
    os.getenv("PROPERTY_ANALYSIS_DATA_LOCATION", "/var/lib/irish_property_analysis/")
    if not TEST_ENV
    else "/tmp/var/lib/irish_property_analysis/"
)

PPR_LOCATION = os.path.join(LISTINGS_DATA_LOCATION, "ppr.csv")

SCHOOLS_DIR_LOCATION = os.path.join(LISTINGS_DATA_LOCATION, "schools")
PRIMARY_SCHOOLS_DATA_LOCATION = os.path.join(SCHOOLS_DIR_LOCATION, "primary.csv")
SECONDARY_SCHOOLS_DATA_LOCATION = os.path.join(SCHOOLS_DIR_LOCATION, "secondary.csv")

BUS_STOP_DIR_LOCATION = os.path.join(LISTINGS_DATA_LOCATION, "bus_stops")
BUS_STOP_DATA_LOCATION = os.path.join(BUS_STOP_DIR_LOCATION, "bus_stops.csv")

os.makedirs(LISTINGS_DATA_LOCATION, exist_ok=True)
os.makedirs(SCHOOLS_DIR_LOCATION, exist_ok=True)
os.makedirs(BUS_STOP_DIR_LOCATION, exist_ok=True)

# Attributes that if they are different on a listing merge attempt we should see at the properties not being mergable
BAD_MERGE_ATTRS = [
    "m_squared",
    "bedrooms",
    "bathrooms",
    "ber",
    "constructed_date",
    "property_type",
    "category",
]

# Attributes that we can merge on if they are different
MERGE_ATTRS = [
    "property_type",
    "clean_agent",
    "bedrooms",
    "bathrooms",
    "category",
    "constructed_date",
    "lat",
    "lng",
    "ber",
    "eircode",
    "m_squared",
    "is_commercial",
    "is_holiday_home",
    "price",
    # "published_date",
]
