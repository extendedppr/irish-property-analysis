import os
import shutil
from pathlib import Path


from irish_property_analysis.settings import (
    PRIMARY_SCHOOLS_DATA_LOCATION,
    SECONDARY_SCHOOLS_DATA_LOCATION,
)


def main():
    resources = os.path.join(Path(__file__).resolve().parents[1], "resources")
    schools = os.path.join(resources, "schools")
    primary = os.path.join(schools, "primary.csv")
    secondary = os.path.join(schools, "secondary.csv")

    shutil.copy(primary, PRIMARY_SCHOOLS_DATA_LOCATION)
    print(f"Wrote: {PRIMARY_SCHOOLS_DATA_LOCATION}")
    shutil.copy(secondary, SECONDARY_SCHOOLS_DATA_LOCATION)
    print(f"Wrote: {SECONDARY_SCHOOLS_DATA_LOCATION}")


if __name__ == "__main__":
    main()
