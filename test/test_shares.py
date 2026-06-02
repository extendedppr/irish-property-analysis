from unittest import TestCase


from irish_property_analysis.shares import ShareObject, ShareDB


class ShareObjectTest(TestCase):
    def test_object_str(self):
        self.assertEqual(
            str(ShareObject()),
            'ShareObject(original_address="None", clean_address="None", county="None", lat="None", lng="None", price="None", clean_agent="None", ber="None", eircode_routing_key="None", m_squared="None", constructed_date="None", beds="None", baths="None", property_type="None", published_date="None")',
        )

    def test_object_serialize(self):
        self.assertEqual(
            ShareObject().serialize(),
            {
                "original_address": None,
                "clean_address": None,
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


class ShareDBTest(TestCase):
    def setUp(self):
        ShareDB().drop_data()

        self.obj_1 = ShareObject()
        self.obj_1.original_address = "test1"
        self.obj_1.clean_address = "test1"
        self.obj_1.county = "dublin"
        self.obj_1.save()

        self.obj_2 = ShareObject()
        self.obj_2.original_address = "test2"
        self.obj_2.clean_address = "test2"
        self.obj_2.county = "cork"
        self.obj_2.save()

    def test_len(self):
        self.assertEqual(len(ShareDB()), 2)

    def test_iter(self):
        self.assertEqual(len(list(ShareDB())), 2)

    def test_filter(self):
        self.assertEqual(len(ShareDB().filter()), 2)

        self.assertEqual(len(ShareDB().filter(county="dublin")), 1)
        self.assertEqual(ShareDB().filter(county="dublin")[0].county, "dublin")
