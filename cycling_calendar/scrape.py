import requests
from lxml import html

DESCRIPTION_XPATHS = [
    '//meta[@name="description"]/@content',
    '//meta[@property="og:description"]/@content',
    '//meta[@name="twitter:description"]/@content',
]


def download_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWeb"
        "Kit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    doc = html.fromstring(response.content)

    return doc


def extract_description(doc):
    for xpath in DESCRIPTION_XPATHS:
        value = doc.xpath(xpath)
        if value:
            return value[0]


def get_description(homepage_url):
    doc = download_page(homepage_url)
    return extract_description(doc).lower() or ""
