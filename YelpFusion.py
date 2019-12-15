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
from bs4 import BeautifulSoup

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from YelpRequestHelper import *

YELP_SEARCH_API_STEP = 50


class YelpFusion:
    def __init__(self):
        self.businesses_set = set([])
        self.current_offset = 0
        self.number_of_business_to_scrape = EnvironmentInit.get_number_of_business_to_scrape()

    def caller_method(self, number_of_business_to_scrape: int):
        while number_of_business_to_scrape > 0:
            if number_of_business_to_scrape > YELP_SEARCH_API_STEP:
                self.get_businesses(YELP_SEARCH_API_STEP, self.current_offset)
            else:
                self.get_businesses(number_of_business_to_scrape, self.current_offset)
            self.current_offset = len(self.businesses_set)
            number_of_business_to_scrape -= YELP_SEARCH_API_STEP

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
        for business in self.businesses_set:
            yelp_review_url = YelpRequestHelper.get_reviews_url_for_business(business)
            response = requests.get(yelp_review_url, headers=YelpRequestHelper.get_request_header())
            # Only proceed if the response code is 200 (SUCCESS)
            if response.status_code == 200:
                response_json = response.json()
                for review in response_json["reviews"]:
                    review_full_url = review["url"]

            else:
                logger.error("HTTP Error while requesting for: {}".format(yelp_review_url))
                logger.error("Response code is: {}".format(response.status_code))
                logger.error("Response: {}".format(response))

    business_full_text_review = {}
    def get_full_text_review(self, full_text_review_url):
        response = requests.get(full_text_review_url)
        if response.status_code == 200:
            beautiful_soup = BeautifulSoup(response.content, "lxml")
            aggregate_rating = beautiful_soup.find("script", {"type": "application/ld+json"}).contents[0]
            aggregate_rating_json = json.loads(aggregate_rating)
            logger.info(aggregate_rating)
            pass
        pass


if __name__ == '__main__':
    t = YelpFusion()
    #t.caller_method(1)
    #t.get_reviews()
    t.get_full_text_review("https://www.yelp.com/biz/kinka-izakaya-original-toronto?adjust_creative=oiO7mo1ABQcXDbWEiGqUdQ&hrid=P3efF6QDMXMW0S9-7qcWxg&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_reviews&utm_source=oiO7mo1ABQcXDbWEiGqUdQ")
