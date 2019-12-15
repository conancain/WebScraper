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
import urllib
from urllib.parse import urlparse

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from YelpRequestHelper import *
from YelpJsonKeys import *

YELP_SEARCH_API_STEP = 50
YELP_REVIEW_PAGE_STEP = 20


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


    def get_full_text_review(self, full_text_review_url):
        o = urlparse(full_text_review_url)
        clean_url = urllib.parse.urlunparse(o._replace(query="start={}"))
        current_review_offset = 0
        is_review_page_empty = False
        business_full_text_review: json = None

        while not is_review_page_empty:
            logger.info("current_review_offset: {}".format(current_review_offset))
            if current_review_offset > MAX_NUMBER_OF_REVIEWS_TO_GET_PER_BUSINESS:
                logger.info("current_review_offset is greater than "
                            "MAX_NUMBER_OF_REVIEWS_TO_GET_PER_BUSINESS: {}".format(
                                MAX_NUMBER_OF_REVIEWS_TO_GET_PER_BUSINESS))
                break
            clean_url_with_page = clean_url.format(current_review_offset)
            response = requests.get(clean_url_with_page)
            if response.status_code == 200:
                beautiful_soup = BeautifulSoup(response.content, "lxml")
                aggregate_rating = beautiful_soup.find("script", {"type": "application/ld+json"}).contents[0]
                aggregate_rating_json = json.loads(aggregate_rating)
                if not business_full_text_review:
                    business_full_text_review = aggregate_rating_json
                else:
                    business_full_text_review[REVIEW].extend(aggregate_rating_json[REVIEW])
                if len(aggregate_rating_json[REVIEW]) == 0:
                    is_review_page_empty = True
                logger.info(aggregate_rating)
                current_review_offset += YELP_REVIEW_PAGE_STEP
                pass
        with open(os.path.join(os.path.dirname(__file__), "output.json"), 'w') as outfile:
            json.dump(business_full_text_review, outfile, indent=4)
        self.transform_output(business_full_text_review)

    def transform_output(self, raw_review_json: json):
        result = []
        with open(os.path.join(os.path.dirname(__file__), "data.json"), 'w') as outfile:
            for review in raw_review_json[REVIEW]:
                rating_value = review[REVIEW_RATING][RATING_VALUE]
                if rating_value > 3:
                    rating = "positive"
                else:
                    rating = "negative"
                result.append([review[DESCRIPTION], rating])
            json.dump(result, outfile, indent=4)


if __name__ == '__main__':
    t = YelpFusion()
    #t.caller_method(1)
    #t.get_reviews()
    t.get_full_text_review("https://www.yelp.com/biz/kinka-izakaya-original-toronto?adjust_creative=oiO7mo1ABQcXDbWEiGqUdQ&hrid=P3efF6QDMXMW0S9-7qcWxg&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_reviews&utm_source=oiO7mo1ABQcXDbWEiGqUdQ")
