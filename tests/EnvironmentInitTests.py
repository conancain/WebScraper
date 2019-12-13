import unittest.mock
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import EnvironmentInit
from EnvironmentInit import *


class EnvironmentInitTests(unittest.TestCase):
    def setUp(self) -> None:
        self.environmentInit = EnvironmentInit()

    def test_yelp_token(self):
        result = self.environmentInit.get_yelp_token()
        self.assertEqual(result, "Your Yelp Developer Token Goes Here")

    def test_yelp_search_url(self):
        result = self.environmentInit.get_yelp_search_url()
        self.assertEqual(result, "https://api.yelp.com/v3/businesses/search?location=Toronto&limit={}&offset={}")

    def test_yelp_review_url(self):
        result = self.environmentInit.get_yelp_review_url()
        self.assertEqual(result, "https://api.yelp.com/v3/businesses/{}/reviews")

    def test_number_of_business_to_scrape(self):
        result = self.environmentInit.get_number_of_business_to_scrape()
        self.assertEqual(result, 1)


if __name__ == '__main__':
    unittest.main()
