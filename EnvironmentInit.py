import os
import json
import sys
import datetime
import logging

from typing import Dict

_config_path = os.path.join(os.path.dirname(__file__), "config.json")
_config_json: Dict[str, object]

logger: logging = None

YELP_TOKEN_KEY = "yelpToken"
YELP_SEARCH_URL_KEY = "yelpSearchUrl"
YELP_REVIEWS_URL_KEY = "yelpReviewsUrl"
NUMBER_OF_BUSINESS_TO_SCRAPE_KEY = "numberOfBusinessToScrape"
MAX_NUMBER_OF_REVIEWS_TO_GET_PER_BUSINESS_KEY = "maxNumberOfReviewsToGetPerBusiness"

YELP_TOKEN: str
YELP_SEARCH_URL: str
YELP_REVIEWS_URL: str
NUMBER_OF_BUSINESS_TO_SCRAPE: int
MAX_NUMBER_OF_REVIEWS_TO_GET_PER_BUSINESS: int

class EnvironmentInit:

    @staticmethod
    def read_config(config_file_full_path: os.path):
        with open(config_file_full_path) as config_file:
            global _config_json
            _config_json = json.load(config_file)

            global YELP_TOKEN
            if YELP_TOKEN_KEY in _config_json:
                YELP_TOKEN = _config_json[YELP_TOKEN_KEY]

            global YELP_SEARCH_URL
            if YELP_SEARCH_URL_KEY in _config_json:
                YELP_SEARCH_URL = _config_json[YELP_SEARCH_URL_KEY]

            global YELP_REVIEWS_URL
            if YELP_REVIEWS_URL_KEY in _config_json:
                YELP_REVIEWS_URL = _config_json[YELP_REVIEWS_URL_KEY]

            global NUMBER_OF_BUSINESS_TO_SCRAPE
            if NUMBER_OF_BUSINESS_TO_SCRAPE_KEY in _config_json:
                NUMBER_OF_BUSINESS_TO_SCRAPE = _config_json[NUMBER_OF_BUSINESS_TO_SCRAPE_KEY]

            global MAX_NUMBER_OF_REVIEWS_TO_GET_PER_BUSINESS
            if MAX_NUMBER_OF_REVIEWS_TO_GET_PER_BUSINESS_KEY in _config_json:
                MAX_NUMBER_OF_REVIEWS_TO_GET_PER_BUSINESS = _config_json[MAX_NUMBER_OF_REVIEWS_TO_GET_PER_BUSINESS_KEY]

        logger.info("EnvironmentInit: _config_json: {}".format(_config_json))

    @staticmethod
    def get_yelp_token() -> str:
        return YELP_TOKEN

    @staticmethod
    def get_yelp_search_url() -> str:
        return YELP_SEARCH_URL

    @staticmethod
    def get_yelp_reviews_url() -> str:
        return YELP_REVIEWS_URL

    @staticmethod
    def get_number_of_business_to_scrape() -> int:
        return NUMBER_OF_BUSINESS_TO_SCRAPE

    @staticmethod
    def get_max_number_of_reviews_to_get_per_business() -> int:
        return MAX_NUMBER_OF_REVIEWS_TO_GET_PER_BUSINESS

    @staticmethod
    def initialize_logger(logging_directory: os.path, log_name: str):
        global logger
        if logger:
            logger.info("EnvironmentInit: Logger is already initialized. Exiting initialize_logger")
            return
        logger = logging.getLogger(log_name)
        logger.setLevel(logging.DEBUG)
        # create file handler which logs even debug messages
        # create logging directory if doesn't exist
        if not os.path.exists(logging_directory):
            os.makedirs(logging_directory)
        fh = logging.FileHandler(
            os.path.join(logging_directory, "{}_{:%Y-%m-%d}.log".format(log_name, datetime.datetime.now())))
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


EnvironmentInit.initialize_logger(os.path.join(os.path.dirname(__file__), "logs"), "YelpFusion")
EnvironmentInit.read_config(_config_path)
