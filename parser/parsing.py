import requests
import json
import time
import re

import unicodedata
import html
from parsing_steps.simple import SimpleParsingStep
import bs4

session = requests.Session()


def normalize(text):
    try:
        if text is None:
            return text
        if isinstance(text, str):
            text = (unicodedata.normalize("NFKD", text)
                               .encode("ascii", "ignore")
                               .decode())
            return re.sub(" +", " ", text)
        raise ValueError("The input text is not a str instance")
    except Exception:
        return text


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
            data["title"] = normalize(block_html.find("h3").get_text())
        except Exception:
            pass

        try:
            page_url = block_html.find("a").get("href", None)
            page_url = page_url.split("/url?q=")[-1].split("&")[0]
            data["url"] = page_url
        except Exception:
            pass

        try:
            description = block_html.find(
                "div", class_="BNeawe s3v9rd AP7Wnd")
            text_from_extended_description = description.find(class_="v9i61e")
            if text_from_extended_description:
                data["description"] = text_from_extended_description.get_text()
            else:
                data["description"] = description.get_text()
            data["description"] = normalize(data["description"])
        except Exception:
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
