import requests
import json
import time

import html
from parsing_steps.simple import SimpleParsingStep
import bs4

session = requests.Session()


class CreateSearchUrlParsingStep(SimpleParsingStep):
    def parse(self, input_data):
        """
        input_data is input text for search request
        """
        base_url = "https://www.google.com/search?q="
        url = base_url + input_data


if __name__ == "__main__":
    search_request = input("enter search request: ")
    CreateSearchUrlParsingStep(input_data=search_request).perform()
