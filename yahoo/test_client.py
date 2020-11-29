from io import StringIO
import unittest

from client import Yahoo


class Test(unittest.TestCase):
    def test_1_1_fetch_price_bad_date(self):
        stonk = ["MSFT", "1950-11-27"]
        expected_price = []
        expected_missed_price = 'failed to retrieve prices for MSFT. Incorrect date format.\nExpected\tYYYY-mm-dd HH:MM:SS\nReceived\t1950-11-27'
    
        Yahoo2 = Yahoo()
        price, missed_price = Yahoo2.fetch_price(stonk)

        self.assertTrue(missed_price)
        self.assertFalse(price)
        self.assertEqual(expected_missed_price, missed_price)
        self.assertEqual(expected_price, price)
    
    def test_1_2_fetch_price_missing_date(self):
        stonk = ["MSFT", "1950-11-27 00:00:00"]
        expected_price = []
        expected_missed_price = 'prices not available for MSFT from 1950-11-27 - 1950-11-29' 
        
        Yahoo2 = Yahoo()
        price, missed_price = Yahoo2.fetch_price(stonk)

        self.assertTrue(missed_price)
        self.assertFalse(price)
        self.assertEqual(expected_missed_price, missed_price)
        self.assertEqual(expected_price, price)

    def test_1_3_fetch_price_success(self):
        stonk = ["MSFT", "2018-11-27 00:00:00"]
        expected_stonk_data = [
            {
                "Date": 103.62382109206798,
                "Open": 104.65743162586419,
                "Low": 102.7364844112807,
                "Close": 104.47216033935547,
                "Volume": 29124500.0,
            },
            {
                "Date": 105.20349064714351,
                "Open": 108.55783550503547,
                "Low": 105.17423885073013,
                "Close": 108.35306549072266,
                "Volume": 46788500.0,
            },
        ]

        Yahoo2 = Yahoo()
        stonk_data, err = Yahoo2.fetch_price(stonk)

        self.assertFalse(err)
        self.assertEqual(err, "")
        self.assertEqual(expected_stonk_data, stonk_data)
        self.assertTrue(stonk_data)

    def test_2_1_fetch_prices_failure(self):
        stonks = [["MSFT", "1950-11-27 00:00:00"], ["TSLA", "1950-11-27 00:00:00"]]
        expected_prices = {}
        expected_missed_prices = {
            "MSFT": "prices not available for MSFT from 1950-11-27 - 1950-11-29",
            "TSLA": "prices not available for TSLA from 1950-11-27 - 1950-11-29",
        }

        Yahoo2 = Yahoo()
        prices, missed_prices = Yahoo2.fetch_prices(stonks)

        self.assertTrue(missed_prices)
        self.assertFalse(prices)
        self.assertEqual(expected_missed_prices, missed_prices)
        self.assertEqual(expected_prices, prices)

    def test_2_2_fetch_prices_hybrid(self):
        stonks = [["MSFT", "2018-11-27 00:00:00"], ["TSLA", "1950-11-27 00:00:00"]]
        expected_prices = {
            "MSFT": [
                {
                    "Date": 103.62382109206798,
                    "Open": 104.65743162586419,
                    "Low": 102.7364844112807,
                    "Close": 104.47216033935547,
                    "Volume": 29124500.0,
                },
                {
                    "Date": 105.20349064714351,
                    "Open": 108.55783550503547,
                    "Low": 105.17423885073013,
                    "Close": 108.35306549072266,
                    "Volume": 46788500.0,
                },
            ],
        }
        expected_missed_prices = {
            "TSLA": "prices not available for TSLA from 1950-11-27 - 1950-11-29"
        }

        Yahoo2 = Yahoo()
        prices, missed_prices = Yahoo2.fetch_prices(stonks)

        self.assertTrue(missed_prices)
        self.assertTrue(prices)
        self.assertEqual(expected_missed_prices, missed_prices)
        self.assertEqual(expected_prices, prices)

    def test_2_3_fetch_prices_success(self):
        stonks = [["MSFT", "2018-11-27 00:00:00"], ["TSLA", "2018-11-27 00:00:00"]]
        expected_prices = {
            "MSFT": [
                {
                    "Date": 103.62382109206798,
                    "Open": 104.65743162586419,
                    "Low": 102.7364844112807,
                    "Close": 104.47216033935547,
                    "Volume": 29124500.0,
                },
                {
                    "Date": 105.20349064714351,
                    "Open": 108.55783550503547,
                    "Low": 105.17423885073013,
                    "Close": 108.35306549072266,
                    "Volume": 46788500.0,
                },
            ],
            "TSLA": [
                {
                    "Date": 68.01000213623047,
                    "Open": 69.39199829101562,
                    "Low": 67.0999984741211,
                    "Close": 68.78399658203125,
                    "Volume": 31791500.0,
                },
                {
                    "Date": 69.197998046875,
                    "Open": 69.65599822998047,
                    "Low": 68.44200134277344,
                    "Close": 69.5739974975586,
                    "Volume": 20638000.0,
                },
            ],
        }
        expected_missed_prices = {}

        Yahoo2 = Yahoo()
        prices, missed_prices = Yahoo2.fetch_prices(stonks)

        self.assertFalse(missed_prices)
        self.assertTrue(prices)
        self.assertEqual(expected_missed_prices, missed_prices)
        self.assertEqual(expected_prices, prices)


# fetch stonk - wrong data format

# fetch - failure
# fetch - hybrid
# fetch - success

# build_stonk_json
#   - failure
#       - log err if incorrect data type
#   - success

if __name__ == "__main__":
    unittest.main()
