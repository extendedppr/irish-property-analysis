from datetime import datetime

import pandas as pd

from irish_property_analysis.settings import BUS_STOP_DATA_LOCATION
from irish_property_analysis.utils import haversine_vectorized, fast_to_dict_records


class BusStops:
    def __init__(self):
        print("Loading Bus Stop Data")
        self.data = pd.read_csv(BUS_STOP_DATA_LOCATION)
        self.data["creation_date"] = self.data["CreationDateTime"].apply(
            lambda x: datetime.strptime(x, "%Y-%m-%dT%H:%M:%S.%f")
        )

    def get_near(self, lat, lng, radius_km=1, before=None):
        data = None
        if before:
            data = self.data[self.data["creation_date"] <= before]
        else:
            data = self.data

        distances = haversine_vectorized(
            lat, lng, data["Latitude"].values, data["Longitude"].values
        )

        mask = distances <= radius_km

        result = (
            data.loc[mask]
            .assign(distance_km=distances[mask])
            .sort_values(by="distance_km")
            .reset_index(drop=True)
        )

        return fast_to_dict_records(result)

    def get_score(self, lat, lng, radius_km=1):
        """
        Get a score for how good a location is for bus stops

        Only gets count now but should factor in a few other things like number of routes
        """
        return len(self.get_near(lat, lng, radius_km=radius_km))


bus_stops = BusStops()
