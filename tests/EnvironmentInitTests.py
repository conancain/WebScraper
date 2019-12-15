import unittest.mock
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import EnvironmentInit
from EnvironmentInit import *


class EnvironmentInitTests(unittest.TestCase):
    def setUp(self) -> None:
        self.environment_init = EnvironmentInit()

    def test_yelp_token(self):
        result = self.environment_init.get_yelp_token()
        self.assertEqual(result, "Your Yelp Developer Token Goes Here")

    def test_yelp_search_url(self):
        result = self.environment_init.get_yelp_search_url()
        self.assertEqual(result, "https://api.yelp.com/v3/businesses/search?location=Toronto&limit={}&offset={}")

    def test_yelp_reviews_url(self):
        result = self.environment_init.get_yelp_reviews_url()
        self.assertEqual(result, "https://api.yelp.com/v3/businesses/{}/reviews")

    def test_number_of_business_to_scrape(self):
        result = self.environment_init.get_number_of_business_to_scrape()
        self.assertEqual(result, 1)

    def test_max_number_of_reviews_to_get_per_business(self):
        result = self.environment_init.get_max_number_of_reviews_to_get_per_business()
        self.assertEqual(result, 500)


if __name__ == '__main__':
    unittest.main()
