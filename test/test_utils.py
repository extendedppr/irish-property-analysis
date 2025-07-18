from unittest import TestCase

import os
import math
import datetime
import random

from irish_property_analysis.utils import (
    read_json,
    mean_data,
    convert_date,
    is_nan,
    is_sale_date_within_range,
)


class UtilsTest(TestCase):
    def test_read_json(self):
        random_file = f"/tmp/{random.random()}"
        with open(random_file, "w") as fh:
            fh.write("[]")
        self.assertEqual(read_json(random_file), [])
        os.remove(random_file)

    def test_mean_data(self):
        data = [{"a": [1, 2], "b": 1}]
        self.assertEqual(mean_data(data, "a")[0]["a"], 1.5)
        self.assertEqual(mean_data(data, "b")[0]["b"], 1)

    def test_convert_date(self):
        self.assertEqual(
            convert_date(datetime.datetime(2025, 1, 1)), datetime.datetime(2025, 1, 1)
        )
        self.assertEqual(
            convert_date(str(datetime.datetime(2025, 1, 1))),
            datetime.datetime(2025, 1, 1),
        )

    def test_is_nan(self):
        self.assertTrue(is_nan(None))
        self.assertTrue(is_nan(math.nan))
        self.assertTrue(is_nan(float("nan")))
        self.assertFalse(is_nan(1))

    def test_is_sale_date_within_range(self):
        self.assertTrue(
            is_sale_date_within_range(
                datetime.datetime(2025, 1, 1), datetime.datetime(2025, 2, 1)
            )
        )
        self.assertFalse(
            is_sale_date_within_range(
                datetime.datetime(2000, 1, 1), datetime.datetime(2025, 2, 1)
            )
        )
