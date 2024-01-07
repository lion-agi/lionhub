import unittest
import datetime

def timestamp_to_datetime(timestamp: int) -> str:
    if isinstance(timestamp, str):
        try:
            timestamp = int(timestamp)
        except ValueError:
            return timestamp
    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

class TestTimestampToDatetime(unittest.TestCase):

    def test_valid_integer_timestamp(self):
        timestamp = 1609459200  # Equivalent to 2021-01-01 00:00:00
        expected_result = '2021-01-01 00:00:00'
        self.assertEqual(timestamp_to_datetime(timestamp), expected_result)

    def test_valid_string_timestamp(self):
        timestamp = '1609459200'  # Equivalent to 2021-01-01 00:00:00
        expected_result = '2021-01-01 00:00:00'
        self.assertEqual(timestamp_to_datetime(timestamp), expected_result)

    def test_invalid_input_non_integer_string(self):
        timestamp = 'not_a_timestamp'
        self.assertEqual(timestamp_to_datetime(timestamp), 'not_a_timestamp')

    def test_invalid_input_non_string(self):
        timestamp = [1609459200]
        with self.assertRaises(TypeError):
            timestamp_to_datetime(timestamp)

if __name__ == '__main__':
    unittest.main()
