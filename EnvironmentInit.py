import os
import json
import sys
import datetime
import logging

from typing import Dict

_config_path = os.path.join(os.path.dirname(__file__), "config.json")
_config_json: Dict[str, object]

logger: logging

YELP_TOKEN_KEY = "yelpToken"
YELP_SEARCH_URL_KEY = "yelpSearchUrl"
YELP_REVIEW_URL_KEY = "yelpReviewUrl"

YELP_TOKEN: str
YELP_SEARCH_URL: str
YELP_REVIEW_URL: str


class EnvironmentInit:
    def __init__(self):
        self.read_config(_config_path)

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

            global YELP_REVIEW_URL
            if YELP_REVIEW_URL_KEY in _config_json:
                YELP_REVIEW_URL = _config_json[YELP_REVIEW_URL_KEY]

    @staticmethod
    def get_yelp_token() -> str:
        return YELP_TOKEN

    @staticmethod
    def get_yelp_search_url() -> str:
        return YELP_SEARCH_URL

    @staticmethod
    def get_yelp_review_url() -> str:
        return YELP_REVIEW_URL

    @staticmethod
    def initialize_logger(logging_directory: os.path, log_name: str):
        global logger
        logger = logging.getLogger("YelpFusion")
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