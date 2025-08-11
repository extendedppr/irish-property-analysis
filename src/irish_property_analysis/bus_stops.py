import pandas as pd

from irish_property_analysis.settings import BUS_STOP_DATA_LOCATION
from irish_property_analysis.utils import haversine_vectorized


class BusStops:
    def __init__(self):
        print("Loading Bus Stop Data")
        self.data = pd.read_csv(BUS_STOP_DATA_LOCATION)

    def get_near(self, lat, lng, radius_km=1):
        distances = haversine_vectorized(
            lat, lng, self.data["Latitude"].values, self.data["Longitude"].values
        )

        mask = distances <= radius_km
        return (
            self.data.loc[mask]
            .assign(distance_km=distances[mask])
            .sort_values(by="distance_km")
            .reset_index(drop=True)
            .to_dict(orient="records")
        )

    def get_score(self, lat, lng, radius_km=1):
        """
        Get a score for how good a location is for bus stops

        Only gets count now but should factor in a few other things like number of routes
        """
        return len(self.get_near(lat, lng))


bus_stops = BusStops()
