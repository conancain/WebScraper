import sys
import os
from typing import Dict

import requests
import datetime
import random
import matplotlib.pyplot as plt
import json
import logging
from pprint import pprint

YELP_TOKEN = r"_4SUttVUeE98iq2GWQd1yrarga2oz-sYvQPlfD6yrxO79fw8FTtbVCBm-_0GmOf7wOxA3btTCgfiV0Hy4iojEtemny1qBBnJmyb9ENLlqF2VCNPDypSTDsQYUBfvXXYx"
YELP_SEARCH_URL = "https://api.yelp.com/v3/businesses/search?location=Toronto&limit={}&offset={}"
YELP_REVIEW_URL = "https://api.yelp.com/v3/businesses/{}/reviews"

NUM_BUSINESSES_TO_SCRAPE = 500

# region Logging Setup
logger = logging.getLogger("YelpFusion")
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
logging_directory = os.path.join(os.path.dirname(__file__), "logs")
# create logging directory if doesn't exist
if not os.path.exists(logging_directory):
    os.makedirs(logging_directory)
fh = logging.FileHandler(os.path.join(logging_directory, "YelpFusion_{:%Y-%m-%d}.log".format(datetime.datetime.now())))
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)
# endregion


class YelpFusion:
    def __init__(self):
        self.businesses_set = set([])
        self.current_offset = 0

    @staticmethod
    def get_request_header() -> Dict[str, str]:
        result: Dict[str, str] = {"Authorization": "Bearer {}".format(YELP_TOKEN)}
        return result

    @staticmethod
    def get_reviews_url_for_business(business_id: str) -> str:
        return YELP_REVIEW_URL.format(business_id)

    @staticmethod
    def get_search_url_for_business(limit: int = 50, offset: int = 0) -> str:
        return YELP_SEARCH_URL.format(limit, offset)

    def get_businesses(self, limit: int = 50, offset: int = 0):
        search_url = self.get_search_url_for_business(limit, offset)
        try:
            logger.info("Sending Request: URL: {}".format(search_url))
            response = requests.get(search_url, headers=self.get_request_header())
            # Only proceed if the response code is 200 (SUCCESS)
            if response.status_code == 200:
                response_json = response.json()
                for business in response_json["businesses"]:
                    business_id = business["id"]
                    if business_id not in self.businesses_set:
                        # Add each business' UID to set
                        self.businesses_set.add(business_id)
            else:
                logger.error("HTTP Error while requesting for: {}".format(search_url))
                logger.error("Response code is: {}".format(response.status_code))
                logger.error("Response: {}".format(response))

            # Once the businesses' UID are added to the set, set the offset to the length of the unique ID already exist
            self.current_offset = len(self.businesses_set)
            logger.info("Request Completed, Response JSON is:")
            logger.info(response.json())
        except Exception as ex:
            logger.error("Error when sending URL: {}".format(search_url))
            logger.error("Response: {}".format(response))
            logger.error(ex, exc_info=True)

    def get_reviews(self):
        print(self.get_request_header())
        pass


if __name__ == '__main__':
    t = YelpFusion()
    t.get_businesses(50, t.current_offset)
