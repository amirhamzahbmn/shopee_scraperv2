from collections import defaultdict
from urllib.parse import quote
from httpx import Client
from parsel import Selector
import time, csv
import numpy as np

# 1. Create HTTP client with headers that look like a real web browser
client = Client(
    headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9,lt;q=0.8,et;q=0.7,de;q=0.6",
    },
    follow_redirects=True,
    http2=True,  # use HTTP/2 
)


def parse_search_results(selector: Selector):
    """parse search results from google search page"""
    results = []
    for box in selector.xpath("//h1[contains(text(),'Search Results')]/following-sibling::div[1]/div"):
        title = box.xpath(".//h3/text()").get()
        url = box.xpath(".//h3/../@href").get()
        text = "".join(box.xpath(".//div[@data-content-feature=1]//text()").getall())
        if not title or not url:
            continue
        url = url.split("://")[1].replace("www.", "")
        results.append((title, url, text))
    return results


def scrape_search(query: str, page=1):
    """scrape search results for a given keyword"""
    # retrieve the SERP
    url = f"https://www.google.com/search?hl=en&q={quote(query)}" + (f"&start={100*(page-1)}" if page > 1 else "") + "&num=100"
    print(f"scraping {query=} {page} of 4")
    results = defaultdict(list)
    response = client.get(url)
    # assert response.status_code200,f"failed status_code={response.status_code}"
    # parse SERP for search result data
    selector = Selector(response.text)
    results["search"].extend(parse_search_results(selector))
    return dict(results)

# example use: scrape 3 pages: 1,2,3
csv_list = []
for page in [1, 2, 3, 4]:
    results = scrape_search('"bicycle" "online shop" site:shopee.com.my', page=page)
    for result in results["search"]:
        print(result)
        csv_list.append(result)

    time.sleep((59-30)*np.random.random()+5) # from 5 to 30 seconds

with open('shopee_shop_list.csv','w', newline='',encoding='utf-8') as f:
	writer=csv.writer(f)
	writer.writerow(['name', 'link'])
	writer.writerows(csv_list)
