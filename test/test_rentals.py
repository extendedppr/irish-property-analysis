from unittest import TestCase

from irish_property_analysis.rentals import RentalObject, RentalDB


class RentalObjectTest(TestCase):
    def setUp(self):
        self.rental_db = RentalDB()
        self.rental_db.drop_data()

    def tearDown(self):
        self.rental_db.close()

    def test_object_str(self):
        self.assertEqual(
            str(RentalObject()),
            'RentalObject(original_address="None", clean_address="None", county="None", lat="None", lng="None", price="None", clean_agent="None", ber="None", eircode_routing_key="None", m_squared="None", constructed_date="None", beds="None", baths="None", property_type="None", published_date="None")',
        )

    def test_save(self):
        self.assertEqual(len(RentalDB()), 0)
        RentalObject(original_address="test1", clean_address="test1").save()
        self.assertEqual(len(RentalDB()), 1)

    def test_serialize(self):
        self.assertEqual(
            RentalObject(original_address="test1", clean_address="test1").serialize(),
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


class RentalDBTest(TestCase):
    def setUp(self):
        RentalDB().drop_data()

    def test_iter(self):
        RentalObject(original_address="test1", clean_address="test1").save()
        RentalObject(original_address="test2", clean_address="test2").save()

        total = 0
        for _ in RentalDB():
            total += 1

        self.assertEqual(total, 2)

    def test_filter(self):
        RentalObject(
            original_address="test1", clean_address="test1", county="dublin"
        ).save()
        RentalObject(
            original_address="test2", clean_address="test2", county="dublin"
        ).save()

        self.assertEqual(len(RentalDB().filter()), 2)
        self.assertEqual(len(RentalDB().filter(address="test1")), 1)
        self.assertEqual(len(RentalDB().filter(address="1", partial=True)), 1)
        self.assertEqual(len(RentalDB().filter(address="test", partial=True)), 2)
        self.assertEqual(len(RentalDB().filter(county="dublin")), 2)
        self.assertEqual(len(RentalDB().filter(county="dub", partial=True)), 2)

        self.assertEqual(len(RentalDB().filter(address_substrs=["test"])), 2)
        self.assertEqual(len(RentalDB().filter(address_substrs=["bad"])), 0)

        self.assertEqual(len(RentalDB().filter(exclude_address_substrs=["bad"])), 2)
        self.assertEqual(len(RentalDB().filter(exclude_address_substrs=["2"])), 1)
