import os

import pandas as pd

from irish_property_analysis.settings import (
    PRIMARY_SCHOOLS_DATA_LOCATION,
    SECONDARY_SCHOOLS_DATA_LOCATION,
)
from irish_property_analysis.utils import haversine_vectorized, fast_to_dict_records


class Schools:
    def __init__(self):
        if not os.path.exists(PRIMARY_SCHOOLS_DATA_LOCATION) or not os.path.exists(
            SECONDARY_SCHOOLS_DATA_LOCATION
        ):
            print("School data not downloaded")
            return

        print("Loading School Data")
        self.primary = pd.read_csv(PRIMARY_SCHOOLS_DATA_LOCATION)
        self.secondary = pd.read_csv(SECONDARY_SCHOOLS_DATA_LOCATION)

        # Headers are a row down
        self.secondary.columns = self.secondary.iloc[0]
        self.secondary = self.secondary.drop(index=0)
        self.secondary = self.secondary.reset_index(drop=True)

        self.secondary["School Latitude"] = pd.to_numeric(
            self.secondary["School Latitude"], errors="coerce"
        )
        self.secondary["School Longitude"] = pd.to_numeric(
            self.secondary["School Longitude"], errors="coerce"
        )

        secondary_coords = self.secondary[["School Latitude", "School Longitude"]]
        primary_coords = self.primary[["School Latitude", "School Longitude"]]

        self.coords_df = pd.concat(
            [secondary_coords, primary_coords], ignore_index=True
        )

    def get_near(self, lat, lng, radius_km=1):
        if not hasattr(self, "primary"):
            return None

        distances = haversine_vectorized(
            lat,
            lng,
            self.coords_df["School Latitude"].values,
            self.coords_df["School Longitude"].values,
        )

        mask = distances <= radius_km

        result = (
            self.coords_df.loc[mask]
            .assign(distance_km=distances[mask])
            .sort_values(by="distance_km")
            .reset_index(drop=True)
        )

        return fast_to_dict_records(result)

    def get_score(self, lat, lng, radius_km=1):
        """
        Get a score for how good a location is for schools

        Only gets count now but should factor in a few other things like number of routes
        """
        if not hasattr(self, "primary"):
            return None
        return len(self.get_near(lat, lng, radius_km=radius_km))


schools = Schools()
