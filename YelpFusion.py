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
import bs4

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from YelpRequestHelper import *


class YelpFusion:
    def __init__(self):
        self.businesses_set = set([])
        self.current_offset = 0

    def get_businesses(self, limit: int = 50, offset: int = 0):
        search_url = YelpRequestHelper.get_search_url(limit, offset)
        try:
            logger.info("Sending Request: URL: {}".format(search_url))
            response = requests.get(search_url, headers=YelpRequestHelper.get_request_header())
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
        print(YelpRequestHelper.get_request_header())
        pass


if __name__ == '__main__':
    t = YelpFusion()
    t.get_businesses(50, t.current_offset)
