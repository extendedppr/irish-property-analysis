from unittest import TestCase

from irish_property_analysis.sales import SaleObject, SaleDB


class SalesObjectTest(TestCase):
    def setUp(self):
        SaleDB().drop_data()

    def test_save(self):
        self.assertEqual(len(SaleDB()), 0)
        SaleObject(original_address="test1", clean_address="test1").save()
        self.assertEqual(len(SaleDB()), 1)

    def test_str(self):
        self.assertEqual(
            str(SaleObject(original_address="test1", clean_address="test1")),
            'SaleObject(original_address="test1", clean_address="test1", county="None", lat="None", lng="None", price="None", clean_agent="None", ber="None", eircode_routing_key="None", m_squared="None", constructed_date="None", beds="None", baths="None", property_type="None", published_date="None")',
        )

    def test_serialize(self):
        self.assertEqual(
            SaleObject(original_address="test1", clean_address="test1").serialize(),
            {
                "original_address": "test1",
                "clean_address": "test1",
                "county": None,
                "lat": None,
                "lng": None,
                "price": None,
                "clean_agent": None,
                "ber": None,
                "eircode_routing_key": None,
                "m_squared": None,
                "constructed_date": None,
                "beds": None,
                "baths": None,
                "property_type": None,
                "published_date": None,
            },
        )


class SalesDBTest(TestCase):
    def setUp(self):
        SaleDB().drop_data()

    def test_iter(self):
        SaleObject(original_address="test1", clean_address="test1").save()
        SaleObject(original_address="test2", clean_address="test2").save()

        total = 0
        for _ in SaleDB():
            total += 1

        self.assertEqual(total, 2)

    def test_filter(self):
        SaleObject(
            original_address="test1", clean_address="test1", county="dublin"
        ).save()
        SaleObject(
            original_address="test2", clean_address="test2", county="dublin"
        ).save()

        self.assertEqual(len(SaleDB().filter()), 2)
        self.assertEqual(len(SaleDB().filter(address="test1")), 1)
        self.assertEqual(len(SaleDB().filter(address="1", partial=True)), 1)
        self.assertEqual(len(SaleDB().filter(address="test", partial=True)), 2)
        self.assertEqual(len(SaleDB().filter(county="dublin")), 2)
        self.assertEqual(len(SaleDB().filter(county="dub", partial=True)), 2)

        self.assertEqual(len(SaleDB().filter(address_substrs=["test"])), 2)
        self.assertEqual(len(SaleDB().filter(address_substrs=["bad"])), 0)
