from unittest import TestCase

import datetime

from irish_property_analysis.ppr_sale import Sale, Sales


class PPRSalesTest(TestCase):
    def setUp(self):
        self.sales = Sales()

        self.sales.append(
            Sale(
                date="01/01/2010",
                address="123 something something street",
                eircode="D02X285",
                county="Dublin",
                price="123,456",
                not_full_market_price="No",
                vat_exclusive="No",
                description_of_property="Second-Hand Dwelling house /Apartment",
                description_of_property_size="greater than or equal to 38 sq metres and less than 125 sq metres",
            )
        )
        self.sales.append(
            Sale(
                date="01/01/2015",
                address="543 place street",
                eircode="D04X285",
                county="Dublin",
                price="1,234,567",
                not_full_market_price="No",
                vat_exclusive="No",
                description_of_property="Second-Hand Dwelling house /Apartment",
                description_of_property_size="greater than or equal to 38 sq metres and less than 125 sq metres",
            )
        )

    def test_filter(self):
        # TODO: partial, also better tests in general

        self.assertEqual(len(self.sales.filter(address="nonexist")), 0)
        self.assertEqual(len(self.sales.filter(address="123")), 1)
        self.assertEqual(len(self.sales.filter(county="dublin")), 2)
        self.assertEqual(len(self.sales.filter(county="cork")), 0)
        self.assertEqual(len(self.sales.filter(address="123", county="dublin")), 1)

    def test_contains(self):
        self.assertTrue(
            Sale(
                date="01/01/2010",
                address="123 something something street",
                eircode="D02X285",
                county="Dublin",
                price="123,456",
                not_full_market_price="No",
                vat_exclusive="No",
                description_of_property="Second-Hand Dwelling house /Apartment",
                description_of_property_size="greater than or equal to 38 sq metres and less than 125 sq metres",
            )
            in self.sales
        )
        self.assertFalse(
            Sale(
                date="01/01/2010",
                address="1234 something something street",
                eircode="D02X285",
                county="Dublin",
                price="123,456",
                not_full_market_price="No",
                vat_exclusive="No",
                description_of_property="Second-Hand Dwelling house /Apartment",
                description_of_property_size="greater than or equal to 38 sq metres and less than 125 sq metres",
            )
            in self.sales
        )


class PPRSaleTest(TestCase):
    def test_init(self):
        self.assertEqual(
            Sale(
                date="01/01/2010",
                address="123 something something street",
                eircode="D02X285",
                county="Dublin",
                price="123,456",
                not_full_market_price="No",
                vat_exclusive="No",
                description_of_property="Second-Hand Dwelling house /Apartment",
                description_of_property_size="greater than or equal to 38 sq metres and less than 125 sq metres",
            ).serialise(),
            {
                "address": "123 something something street",
                "county": "dublin",
                "date": datetime.datetime(2010, 1, 1, 0, 0),
                "description_of_property": "second_hand",
                "description_of_property_size": ">38sm <125sqm",
                "eircode": "D02X285",
                "eircode_routing_key": "d02",
                "eircode_unique_id": "x285",
                "not_full_market_price": "No",
                "price": 123456.0,
                "vat_exclusive": "No",
            },
        )

    def test_parse(self):
        self.assertEqual(
            Sale.parse(
                Sale(
                    date="01/01/2010",
                    address="123 something something street",
                    eircode="D02X285",
                    county="Dublin",
                    price="123,456",
                    not_full_market_price="No",
                    vat_exclusive="No",
                    description_of_property="Second-Hand Dwelling house /Apartment",
                    description_of_property_size="greater than or equal to 38 sq metres and less than 125 sq metres",
                )
            ).hash,
            Sale(
                date="01/01/2010",
                address="123 something something street",
                eircode="D02X285",
                county="Dublin",
                price="123,456",
                not_full_market_price="No",
                vat_exclusive="No",
                description_of_property="Second-Hand Dwelling house /Apartment",
                description_of_property_size="greater than or equal to 38 sq metres and less than 125 sq metres",
            ).hash,
        )
        self.assertEqual(
            Sale.parse(
                {
                    "date": "01/01/2010",
                    "address": "123 something something street",
                    "eircode": "D02X285",
                    "county": "Dublin",
                    "price": "123,456",
                    "not_full_market_price": "No",
                    "vat_exclusive": "No",
                    "description_of_property": "second_hand",
                    "description_of_property_size": ">38sm <125sqm",
                }
            ).hash,
            Sale(
                date="01/01/2010",
                address="123 something something street",
                eircode="D02X285",
                county="Dublin",
                price="123,456",
                not_full_market_price="No",
                vat_exclusive="No",
                description_of_property="Second-Hand Dwelling house /Apartment",
                description_of_property_size="greater than or equal to 38 sq metres and less than 125 sq metres",
            ).hash,
        )

    def test_eircode_routing_key(self):
        self.assertEqual(
            Sale(
                date="01/01/2010",
                address="123 something something street",
                eircode="D02X285",
                county="Dublin",
                price="123,456",
                not_full_market_price="No",
                vat_exclusive="No",
                description_of_property="Second-Hand Dwelling house /Apartment",
                description_of_property_size="greater than or equal to 38 sq metres and less than 125 sq metres",
            ).eircode_routing_key,
            "d02",
        )

        self.assertEqual(
            Sale(
                date="01/01/2010",
                address="123 something something street",
                eircode=None,
                county="Dublin",
                price="123,456",
                not_full_market_price="No",
                vat_exclusive="No",
                description_of_property="Second-Hand Dwelling house /Apartment",
                description_of_property_size="greater than or equal to 38 sq metres and less than 125 sq metres",
            ).eircode_routing_key,
            None,
        )

        self.assertEqual(
            Sale(
                date="01/01/2010",
                address="123 something something street",
                eircode="",
                county="Dublin",
                price="123,456",
                not_full_market_price="No",
                vat_exclusive="No",
                description_of_property="Second-Hand Dwelling house /Apartment",
                description_of_property_size="greater than or equal to 38 sq metres and less than 125 sq metres",
            ).eircode_routing_key,
            None,
        )

    def test_eircode_unique_id(self):
        self.assertEqual(
            Sale(
                date="01/01/2010",
                address="123 something something street",
                eircode="D02X285",
                county="Dublin",
                price="123,456",
                not_full_market_price="No",
                vat_exclusive="No",
                description_of_property="Second-Hand Dwelling house /Apartment",
                description_of_property_size="greater than or equal to 38 sq metres and less than 125 sq metres",
            ).eircode_unique_id,
            "x285",
        )

        self.assertEqual(
            Sale(
                date="01/01/2010",
                address="123 something something street",
                eircode=None,
                county="Dublin",
                price="123,456",
                not_full_market_price="No",
                vat_exclusive="No",
                description_of_property="Second-Hand Dwelling house /Apartment",
                description_of_property_size="greater than or equal to 38 sq metres and less than 125 sq metres",
            ).eircode_unique_id,
            None,
        )

        self.assertEqual(
            Sale(
                date="01/01/2010",
                address="123 something something street",
                eircode="",
                county="Dublin",
                price="123,456",
                not_full_market_price="No",
                vat_exclusive="No",
                description_of_property="Second-Hand Dwelling house /Apartment",
                description_of_property_size="greater than or equal to 38 sq metres and less than 125 sq metres",
            ).eircode_unique_id,
            None,
        )
