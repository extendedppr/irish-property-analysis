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
    remove_duplicates,
    chunks,
    none_to_str,
    minimize_str,
    write_to_csv,
    read_csv_to_dict,
)


class UtilsTest(TestCase):
    def test_write_to_csv(self):
        random_file = f"/tmp/{random.random()}"
        write_to_csv(random_file, [{"a": 1, "b": 2}, {"a": 3, "b": 4}])
        self.assertEqual(
            read_csv_to_dict(random_file), [{"a": "1", "b": "2"}, {"a": "3", "b": "4"}]
        )

    def test_read_csv_to_dict(self):
        random_file = f"/tmp/{random.random()}"
        write_to_csv(random_file, [{"a": 1, "b": 2}, {"a": 3, "b": 4}])
        self.assertEqual(
            read_csv_to_dict(random_file), [{"a": "1", "b": "2"}, {"a": "3", "b": "4"}]
        )
        self.assertEqual(
            read_csv_to_dict(random_file, headers=["y", "z"]),
            [{"y": "1", "z": "2"}, {"y": "3", "z": "4"}],
        )

    def test_read_json(self):
        random_file = f"/tmp/{random.random()}"
        with open(random_file, "w") as fh:
            fh.write("[]")
        self.assertEqual(read_json(random_file), [])
        os.remove(random_file)
        with self.assertRaises(FileNotFoundError):
            read_json(random_file)

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
        self.assertEqual(
            convert_date("2026-01-01 00:00:00.000"),
            datetime.datetime(2026, 1, 1),
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

    def test_remove_duplicates(self):
        self.assertEqual(
            remove_duplicates([{"a": 1}, {"a": 1}, {"a": 2}]), [{"a": 1}, {"a": 2}]
        )

    def test_remove_duplicates_subset_fields(self):
        self.assertEqual(
            remove_duplicates(
                [{"a": 1, "b": 1}, {"a": 1, "b": 2}, {"a": 2, "b": 3}],
                subset_fields=["b"],
            ),
            [{"a": 1, "b": 1}, {"a": 1, "b": 2}, {"a": 2, "b": 3}],
        )

    def test_chunks(self):
        self.assertEqual(chunks([1, 2, 3, 4, 5], 2), [[1, 2], [3, 4], [5]])

    def test_none_to_str(self):
        self.assertEqual(none_to_str("abc"), "abc")
        self.assertEqual(none_to_str(None), "")

    def test_minimize_str(self):
        self.assertEqual(minimize_str("abc", length=10), "abc")
        self.assertEqual(minimize_str("abcdefg", length=5), "ab...")
        self.assertEqual(minimize_str("abcde", length=5), "abcde")
        self.assertEqual(minimize_str("abc  def", length=10), "abc def")
