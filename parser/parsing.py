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
        yield DownloadSearchDataParsingStep({
            "url": url,
            "start_position": 1,
        })


class DownloadSearchDataParsingStep(SimpleParsingStep):
    def download_data(self, url):
        """
        url is downloading url.
        Returns html if success downloading
        """
        time.sleep(1)
        headers = {'Accept-Encoding': 'identity'}
        return html.unescape(session.get(url, headers=headers).text)

    def get_result_data(self, block_html, position):
        """
        html is div html for 1 block result
        """
        data = dict()

        try:
            data["title"] = block_html.find("h3").get_text()
        except Exception:
            pass

        try:
            data["url"] = block_html.find("a").get("href", None)
        except:
            pass

        try:
            data["description"] = block_html.find(
                "div", class_="kCrYT").next().find("div", class_="sCuL3").get_text()
        except:
            pass

        data["position"] = position
        return data

    def get_next_page_url(self, page_element):
        try:
            return "https://google.com" + page_element.find(class_="nBDE1b G5eFlf").get("href", None)
        except:
            pass


    def parse(self, input_data):
        """
        input_data is dict: {
            "url": str,
            "start_position": int,
        }
        """
        url = input_data["url"]
        html = self.download_data(url)
        soup = bs4.BeautifulSoup(html, "lxml")

        data_divs = soup.find_all(
            "div", class_="Gx5Zad fP1Qef xpd EtOod pkphOe")
        start_position = input_data.get("start_position", 1)
        for position, block_html in enumerate(data_divs, start=start_position):
            if position > 100:
                break




if __name__ == "__main__":
    search_request = input("enter search request: ")
    CreateSearchUrlParsingStep(input_data=search_request).perform()
