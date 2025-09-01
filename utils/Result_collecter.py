from bs4 import BeautifulSoup
import requests
import re


def total_results(search_query:str):
    url = f"https://www.olx.ba/pretraga?q={search_query.replace(' ', '+')}&category_id=1"
    headers = {"User-Agent": "Mozilla/5.0"}

    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    # Find the <h1 class="search-title"> element
    total_results = 0
    h1 = soup.find("h1", class_="search-title")
    if h1:
        b_tag = h1.find("b")
        if b_tag:
            matches = re.findall(r"\d[\d\.]*", b_tag.text)
            if matches:
                total_results = int(matches[-1].replace('.', ''))
    return total_results