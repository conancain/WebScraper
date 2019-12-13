import unittest.mock
from unittest.mock import patch
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import YelpRequestHelper
from YelpRequestHelper import *


class YelpRequestHelperTests(unittest.TestCase):
    def setUp(self) -> None:
        self.yelp_request_helper = YelpRequestHelper()

    def test_request_header(self):
        with patch.object(EnvironmentInit, 'get_yelp_token') as mock_yelp_token:
            mock_yelp_token.return_value = "TESTTOKEN123!@#"
            result = YelpRequestHelper.get_request_header()
            self.assertEqual(result, {"Authorization": "Bearer TESTTOKEN123!@#"})

    def test_reviews_url_for_business(self):
        with patch.object(EnvironmentInit, 'get_yelp_reviews_url') as mock_yelp_reviews_url:
            mock_yelp_reviews_url.return_value = "https://api.yelp.com/v3/businesses/{}/reviews"
            result = YelpRequestHelper.get_reviews_url_for_business("Business123")
            self.assertEqual(result, "https://api.yelp.com/v3/businesses/Business123/reviews")

    def test_search_url_for_business(self):
        with patch.object(EnvironmentInit, 'get_yelp_search_url') as mock_yelp_search_url:
            mock_yelp_search_url.return_value = "https://api.yelp.com/v3/businesses/search?location=Toronto&limit={}&offset={}"
            result = YelpRequestHelper.get_search_url(12, 23)
            self.assertEqual(result, "https://api.yelp.com/v3/businesses/search?location=Toronto&limit=12&offset=23")


if __name__ == '__main__':
    unittest.main()
