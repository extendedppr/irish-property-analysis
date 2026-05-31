import tempfile
import os
import datetime

from unittest import TestCase
from unittest.mock import patch


TEST_DATA = """AtcoCode,PlateCode,CommonName,ShortCommonName,CommonNameGA,ShortCommonNameGA,Indicator,Street,NptgLocalityRef,Easting,Northing,Latitude,Longitude,StopType,BusStopType,TimingStatus,CompassPoint,StopAreaRef,AdministrativeAreaRef,Status,CreationDateTime,ModificationDateTime
7010PB003857,,Ballymagrorty,Ballymagrorty,B Mhic Robhartaigh,B Mhic Robhartaigh,Near,,E0701003,641057,920841,55.0334043,-7.3577718,BCT,CUS,OTH,NW,,701,inactive,1969-12-31T00:00:00.000,2021-06-01T16:08:18.000
7010PB003858,,Coshquin,,,,Nr,,E0701003,641054,920860,55.0335753,-7.3578159,BCT,CUS,OTH,N,,701,active,1969-12-31T00:00:00.000,2016-10-28T15:12:27.000
7010PB003859,,Culmore Point,,,,Opp,Culmore Road,E0701003,646370,922263,55.0457123,-7.2744401,BCT,CUS,OTH,N,,701,active,1969-12-31T00:00:00.000,1969-12-31T23:00:00.000
7010PB003860,,Culmore Point,,,,o/s,Culmore Road,E0701003,646379,922262,55.0457025,-7.2742994,BCT,CUS,OTH,N,,701,active,1969-12-31T00:00:00.000,1969-12-31T23:00:00.000
7010B158131,158131.0,Ulsterbus Depot,Ulsterbus Depot,Busáras Ulsterbus,Busáras Ulsterbus,,,E0701001,643648,916772,54.9966288,-7.3178663,BCT,MKD,OTH,N,,701,active,2000-01-01T00:00:00.000,2021-06-17T18:10:53.000
701000002,12537.0,Derry Patrick Street,Derry Patrick St,Doire Sráid Phádraig,Doire Sr Phádraig,,,E0701001,643358,917142,54.99998,-7.32234,BCT,MKD,OTH,N,,701,active,2020-05-07T00:00:00.000,2024-11-07T10:40:10.001
701000001,13223.0,Water Street,Water Street,Sráid an Uisce,Sráid an Uisce,,,E0701001,643683,916710,54.9960687,-7.3173289,BCT,CUS,OTH,N,,701,active,2016-10-04T00:00:00.000,2025-05-12T14:18:52.882
701000004,,Dungiven,Dungiven,Dún Geimhin,Dún Geimhin,,,E0701001,669220,909127,54.9250579,-6.9201336,BCT,MKD,OTH,S,,701,active,2019-10-18T00:00:00.000,2021-06-28T12:45:01.000
701000005,,Dungiven,Dungiven,Dún Geimhin,Dún Geimhin,,,E0701001,669288,909066,54.9245005,-6.9190877,BCT,MKD,OTH,N,,701,active,2019-10-18T00:00:00.000,2021-06-28T12:45:39.000"""


class BusStopTest(TestCase):
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(
            delete=False, suffix=".csv", mode="w", encoding="utf-8"
        )
        self.temp_file.write(TEST_DATA)
        self.temp_file_path = self.temp_file.name
        self.temp_file.close()

    def tearDown(self):
        if os.path.exists(self.temp_file_path):
            os.remove(self.temp_file_path)

    def test_get_near_before(self):
        with patch(
            "irish_property_analysis.settings.BUS_STOP_DATA_LOCATION",
            self.temp_file_path,
        ):
            from irish_property_analysis.bus_stops import bus_stops

            self.assertEqual(
                len(
                    bus_stops.get_near(
                        55.0335753,
                        -7.3578159,
                        radius_km=99999,
                        before=datetime.datetime(2000, 1, 1),
                    )
                ),
                4,
            )

    def test_get_near(self):
        with patch(
            "irish_property_analysis.settings.BUS_STOP_DATA_LOCATION",
            self.temp_file_path,
        ):
            from irish_property_analysis.bus_stops import bus_stops

            self.assertEqual(
                len(bus_stops.get_near(55.0335753, -7.3578159, radius_km=99999)), 8
            )

            self.assertEqual(
                len(bus_stops.get_near(55.0335753, -7.3578159, radius_km=0.01)), 1
            )

    def test_get_score(self):
        with patch(
            "irish_property_analysis.settings.BUS_STOP_DATA_LOCATION",
            self.temp_file_path,
        ):
            from irish_property_analysis.bus_stops import bus_stops

            self.assertEqual(
                bus_stops.get_score(55.0335753, -7.3578159, radius_km=99999),
                8,
            )

            self.assertEqual(
                bus_stops.get_score(55.0335753, -7.3578159, radius_km=0.01),
                1,
            )
