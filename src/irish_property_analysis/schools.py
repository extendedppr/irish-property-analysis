import pandas as pd

from irish_property_analysis.settings import (
    PRIMARY_SCHOOLS_DATA_LOCATION,
    SECONDARY_SCHOOLS_DATA_LOCATION,
)
from irish_property_analysis.utils import haversine_vectorized


class Schools:
    def __init__(self):
        print("Loading School Data")
        self.primary = pd.read_csv(PRIMARY_SCHOOLS_DATA_LOCATION)
        self.secondary = pd.read_csv(SECONDARY_SCHOOLS_DATA_LOCATION)

    def get_near(self, lat, lng, radius_km=1):
        final_data = []

        for idx, data in enumerate([self.primary, self.secondary]):
            if idx == 1:
                data.columns = data.iloc[0]
                data = data.drop(index=0)
                data = data.reset_index(drop=True)

                data["School Latitude"] = pd.to_numeric(
                    data["School Latitude"], errors="coerce"
                )
                data["School Longitude"] = pd.to_numeric(
                    data["School Longitude"], errors="coerce"
                )

            distances = haversine_vectorized(
                lat,
                lng,
                data["School Latitude"].values,
                data["School Longitude"].values,
                radius_km=radius_km,
            )

            mask = distances <= radius_km
            final_data.extend(
                data.loc[mask]
                .assign(distance_km=distances[mask])
                .sort_values(by="distance_km")
                .reset_index(drop=True)
                .to_dict(orient="records")
            )

        return final_data

    def get_score(self, lat, lng, radius_km=1):
        """
        Get a score for how good a location is for schools

        Only gets count now but should factor in a few other things like number of routes
        """
        return len(self.get_near(lat, lng))


schools = Schools()
