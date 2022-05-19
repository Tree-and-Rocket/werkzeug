
"""Simple command-line example for Custom Search.
Command-line application that does a search.
"""

import pprint
import requests
from googleapiclient.discovery import build



i = 0
def pull(urls):
    global i
    for url in urls:
        nr = str(i)
        while len(nr) < 6:
            nr = "0" + nr

        f = open("images/" + nr + '.jpg','wb')
        f.write(requests.get(url).content)
        f.close()
        i += 1


def get_urls(pages):
    urls = []
    for page in pages:
        idx = page.rfind("View full size")
        cut1 = page[:idx]
        idx1 = page.rfind('id="largerlink"')
        cut2 = cut1[idx1+22:-2]
        urls.append(cut2)
        print(cut2)
    return urls

def api():
    # Build a service object for interacting with the API. Visit
    # the Google APIs Console <http://code.google.com/apis/console>
    # to get an API key for your own application.
    service = build(
        "customsearch", "v1", developerKey=""
    )

    res = (
        service.cse()
        .list(
            q="accident",
            cx="cd13e31dfc0529a86",
            imgSize="HUGE"
        )
        .execute()
    )
    htmls = []
    for item in res["items"]:
        h = requests.get(item['link']).content.decode("utf-8") 
        print(type(h))

        htmls.append(h)

    return htmls

if __name__ == "__main__":

    pages = api()
    imageurls = get_urls(pages)
    pull(imageurls)