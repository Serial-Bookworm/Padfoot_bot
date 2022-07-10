import re
import requests
from bs4 import BeautifulSoup

from botutils.constants import IS_URL_REGEX


def get_ffn_url_from_query(query):
    ffn_list = []
    href = []

    url = 'https://www.google.com/search?q=' + \
        query+"+fanfiction"

    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')
    found = soup.findAll('a')

    for link in found:
        href.append(link['href'])

    for i in range(len(href)):
        if re.search(r"fanfiction.net/s/", href[i]) is not None:
            ffn_list.append(href[i])

    if not ffn_list:
        return None

    ffn_url = re.search(IS_URL_REGEX, ffn_list[0])

    return ffn_url.group(0)


def get_ao3_url_from_query(query):
    ao3_list = []
    href = []

    url = 'https://www.google.com/search?q=' + \
        query+"+archiveofourown"

    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')
    found = soup.findAll('a')
    for link in found:
        href.append(link['href'])

    for i in range(len(href)):

        # append /works/ first
        if re.search(r"\barchiveofourown.org/works/\b", href[i]) is not None:
            ao3_list.append(href[i])

        # append /chapters/ next
        if re.search(r"\barchiveofourown.org/chapters/\b", href[i]) is not None:
            ao3_list.append(href[i])


    if not ao3_list:
        return None

    ao3_url = re.search(IS_URL_REGEX, ao3_list[0])

    return ao3_url.group(0)
