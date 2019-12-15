import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from EnvironmentInit import *


class YelpRequestHelper:
    @staticmethod
    def get_request_header() -> Dict[str, str]:
        result: Dict[str, str] = {"Authorization": "Bearer {}".format(EnvironmentInit.get_yelp_token())}
        return result

    @staticmethod
    def get_reviews_url_for_business(business_id: str) -> str:
        yelp_reviews_url = EnvironmentInit.get_yelp_reviews_url()
        return yelp_reviews_url.format(business_id)

    @staticmethod
    def get_search_url(limit: int = 50, offset: int = 0) -> str:
        yelp_search_url = EnvironmentInit.get_yelp_search_url()
        return yelp_search_url.format(limit, offset)

    @staticmethod
    def log_request_error(clean_url_with_page, response):
        logger.error("HTTP Error while requesting for: {}".format(clean_url_with_page))
        logger.error("Response code is: {}".format(response.status_code))
        logger.error("Response: {}".format(response))