from seleniumwire import webdriver #Just to grab fetch requests of the api
import requests, csv, time
import pandas as pd

# Create a new instance of the Chrome driver
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)

MAX_SHOPS_PER_BROWSER = 20

my_headers = {
    "cookie": "_gcl_au=1.1.1567843092.1685679537; _fbp=fb.2.1685679538053.1872637326; SPC_F=rwDSKiCdQ5e3HU1Cltv8PFqQIG0BxgPX; REC_T_ID=982e8b58-00fc-11ee-b3ef-2cea7fac23b0; language=en; SPC_CLIENTID=cndEU0tpQ2RRNWUzjyszrqmkesspknib; _ga_H06K3499BD=GS1.1.1686718742.8.0.1686718742.60.0.0; SPC_SI=vzi2ZAAAAABkNWZ5REt2ZZh0gQAAAAAAUE1mY3liaFk=; _gid=GA1.3.566623019.1690279472; SPC_ST=.dlRRYlJNSHFLUTBUUEdwepkgkDt0EI0gL4zlLlaSdz0ijaRSWIAKlNZjU2yVaV8CmBHIVkF1NsOju2Jb+GDBJCZ0NYP4F3tfQltNInOuOzhVBMsNQ2ZGYVjasY31vrdNWqBzqGapsvMQiPYHk+OkQ9UpKB+FIuebIDK7MjUsF+2umHycsZ5cd1TmPwYjYUsgI+U3jpflK5Xe2aABpH62TA==; SPC_U=1010837601; SPC_R_T_IV=S2ZPV1FWTVRpUXRldTFsQg==; SPC_T_ID=jz6K5nJ9xxfrd063nvg1ANDfd4Eclxps/LxdcMeFesBm3ajc20pV2iiapf5/oa4G6tGhvVJGukANzuMTfRCF8HtffMHTSh+E40VLxCQSvU1evaOSMyBmxLVdiIsWu/3xmWeGg+ou44ykg0rSTVnUXC9ydsuXRgkGooKmT5VEA68=; SPC_T_IV=S2ZPV1FWTVRpUXRldTFsQg==; SPC_R_T_ID=jz6K5nJ9xxfrd063nvg1ANDfd4Eclxps/LxdcMeFesBm3ajc20pV2iiapf5/oa4G6tGhvVJGukANzuMTfRCF8HtffMHTSh+E40VLxCQSvU1evaOSMyBmxLVdiIsWu/3xmWeGg+ou44ykg0rSTVnUXC9ydsuXRgkGooKmT5VEA68=; AMP_TOKEN=%24NOT_FOUND; _QPWSDCXHZQA=0f115e16-cf18-4667-c388-287b39d0aa35; __LOCALE__null=MY; csrftoken=p01tmQbTynXUOdbVeT2TbVbyqDc51BqZ; _ga=GA1.1.851799232.1685679542; _ga_NEYMG30JL4=GS1.1.1690344627.5.1.1690346615.0.0.0; shopee_webUnique_ccd=iMabb3AJ%2BBfwBC0zrofRqQ%3D%3D%7CsKl3qi1xV%2B2RqWH2KwZ0KqXhrpcAWCIhc08LizLK9eIS8OTO2fqRyEBwAp2QlZhOEpZDPj8DGxUERNb3U3hRmbtk5Bq6zFeuQ5Q%3D%7CjYx6eup1SJJloxPe%7C06%7C3; ds=60b93f662dfee03994bf255a3cbec4f3; SPC_EC=SU5Mb0FwbXV3QllHT1lqYnlIG6skoNk+mZ58nwPdx6ZrXJ6ZbdKkPkh8yfjYKfzvkxJBo4T7GXXLTdk5PuDQm1fMRjHqcgK+Fu6MrRly4f1gyBSCZRBKrh1PE6NuZ7bVzw+jBjacduZ+ezY3qzftvWJQtWiBFvds7UbYbAnyTuI=",
    "1c588bfb": """?Qm:@?#Q$j=OWCti"tMr6IMe+""",
    "37244b32": """;jM(m8u%VlAtkN2g1F#bI,'@9V$d'[f>h3>1.B6=hoE[;o:a-E9JR1Y0-C&&m$[*2;\\o`@S0OG_hd7_fQGYO\\L,3G6f7'SR_X^VI@@2"S(9?`a`scJqo9'F<;dA9V[OlNPc*U7e1(5K<HR&069XkHlZVtkP>Oq_1.g.M(0$\u0021<P%d=,\u0021-jdM;M5BF?bOalPd-Xu[qM3\\Q1jfiGH3?WT^\u0021fJf5n(0A?jRmH(*%:WlfUVhq^[\u00215"<n`S5?lJV,Qk\u0021YN[to%.""_,O)L=gRm;a)VBlk0*V32[A:S9K4<W9IPkj([/*E$ef?f5%3Kj,dVcNHD9]<fqftH:q%Wd0^nBT$;cu1XZ`3$O2#5bI_Q`5LQMKV$c#El>E>6li+BNaDf[VLE=*WQBV""",
    "4417d2d3": """1Nsq,\;a"BNU$aP*+fDL<0S2?""",
    "authority": "shopee.com.my",
    "accept": "application/json",
    "accept-language": "en-US,en;q=0.9",
    "af-ac-enc-dat": "AAcyLjkuMi0yAAABiZCCfFYAABBjA0AAAAAAAAAAAj+vsCOmPFyU/ytSpbZSLToKuPUCmKy8QIQFjQpAbY2iCRKRWopsJISKtYmJ07GBefN8ulzljhT4VpQxJ0QAzwBzWGRJZeB4niJsodp8qGzUIvrk/FYHQorJG+uKshzY6emgZaWnoLUg6SWs58zAWxQvlVY9XfVkXOhIQprmC9BaT07CxsIGr4KJwIRehQpEVU1+MZ8+AAS4ju9MetjZ7bw/QSkA4FAzKxF+WYL4O5NQfZ36h0HRRL59yjk/y32rBVFClhd3yxrxaPonttVX7/GXGzr86RW9HWYKa5hyZHCySL6a4+d1BnLvj2UItT6b163sOnJGc28B+t9ytSK/p3Y8mZ5V6augFZWgtdTqADsJNBWM7JKH39HuknHrErW7chbmKEYtRiKyJacEO9+FyCbhwQ3ioOazXMX0kCH6nPVgtuyzYEOtLFrStzdhXF29+0B32RxhxUIz0do6u968tgyX47uXl/82EyfDx/bVRcPaaRvYmx2Y+/zgdhRdu9PxTriOhQR2+vHZwM0CH9aJrMyByAHYilagjeXO+g8oPH3pZVAHEd+fd5/7GiQshNzRuouKF1VRAl+rcrUAbUSko7rXqS2LBtjs/0ocwvppC0XgWUp3rGN1WkDprtEzAf/wcum20WBRAl+rcrUAbUSko7rXqS2LBtjs/0ocwvppC0XgWUp3rB0Dzp9DbD2qNGokICRtVPiuk6yQ5P3eFusPDVX5LmiNCw1e2zkbICMjy+cYi27Y02GH/CbqAxoueRJl+EtJRok3k3A7W2PlGAjot5pwPCgnCw1e2zkbICMjy+cYi27Y06V4ai8wvqv8TIeb9X8H577UIP2LvKQ6TekFuQLtvQIQT14xBhlstwzFVbpGSg7PtkS/fcw7szUA1Edlr/Bs/xnbCQ8ILFHXpLC/t2yB85e5l/82EyfDx/bVRcPaaRvYm5f/NhMnw8f21UXD2mkb2JuJlpGDDsXihA8s80ht/5CJTdcbW+AAsWLz8YEN3WYUXvgf8tZbjjUydGoKMciASUAe3O1CR9esy//LuimI1T2e/q8xv3EJaDVWNiy3UwxAZ0gD9O1aYGgjmjuYbekv+r9Y7mwurx0dJIfjzU0b5dn0",
    "af-ac-enc-sz-token": "iMabb3AJ+BfwBC0zrofRqQ==|sKl3qi1xV+2RqWH2KwZ0KqXhrpcAWCIhc08LizLK9eIS8OTO2fqRyEBwAp2QlZhOEpZDPj8DGxUERNb3U3hRmbtk5Bq6zFeuQ5Q=|jYx6eup1SJJloxPe|06|3",
    "content-type": "application/json",
    "referer": "https://shopee.com.my/",
    "sec-ch-ua": '""Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115""',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Linux"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "x-api-source": "pc",
    "x-csrftoken": "p01tmQbTynXUOdbVeT2TbVbyqDc51BqZ",
    "x-requested-with": "XMLHttpRequest",
    "x-sap-ri": "7aa4c064b09fb6306463dd365ce5c94032869bc21c107a67",
    "x-shopee-language": "en",
    "x-sz-sdk-version": "2.9.2-2&1.4.1"
}

def create_new_browser_instance():
    global driver
    driver.quit()
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    print("Creating new browser instance to alleviate resources..")

def read_shop_list():

    with open("shopee_shop_list.csv","r", newline='') as f:
        links = csv.reader(f, delimiter=',')
        for row in links:
            yield(row[1])

def fetch_api(url):
    driver.get("https://" + url)
    time.sleep(5)
    shop_api = ''
    for request in driver.requests:
        if request.response:
            if str(request).find('shop_base') != -1:
                shop_api = request
    return str(shop_api)

def get_shop_data(shop_list, api_url):

    url = api_url

    headers = my_headers

    response = requests.request("GET", url, headers=headers)

    data = response.json()

    print(f"Found {data['data'].get('name')}!")

    shop_list.append(data['data'])

    return data['data'].get('shopid')

def get_total_item_count(shop_id):

    url = "https://shopee.com.my/api/v4/shop/rcmd_items"

    querystring = {"bundle":"shop_page_category_tab_main","limit":"1","offset":"0","shop_id":shop_id,"sort_type":"1","upstream":""}

    headers = my_headers

    response = requests.request("GET", url, headers=headers, params=querystring)

    data = response.json()
    item_count = data['data'].get('total')

    return item_count

def get_product_listings(product_list, n, shop_id, inactive_shops):

    url = "https://shopee.com.my/api/v4/shop/rcmd_items"

    querystring = {"bundle":"shop_page_category_tab_main","limit":"100","offset":n*100,"shop_id":shop_id,"sort_type":"1","upstream":""}

    headers = my_headers

    response = requests.request("GET", url, headers=headers, params=querystring)

    data = response.json()

    try:
        for product in data['data']['items']:
            product_list.append(product)
    except:
        print("No products found, shop inactive")
        inactive_shops.append(shop_id)

def get_total_soldout_item_count(shop_id):
    url = "https://shopee.com.my/api/v4/shop/search_items"

    querystring = {"filter_sold_out":"1","limit":"1","offset":"0","order":"desc","shopid":shop_id,"sort_by":"pop","use_case":"4"}

    headers = my_headers

    response = requests.request("GET", url, headers=headers, params=querystring)

    data = response.json()
    soldout_item_count = data.get('total_count')

    return soldout_item_count

def get_soldout_product_listings(soldout_product_list, n, shop_id):
    url = "https://shopee.com.my/api/v4/shop/search_items"

    querystring = {"filter_sold_out":"1","limit":"100","offset":n*100,"order":"desc","shopid":shop_id,"sort_by":"pop","use_case":"4"}

    headers = my_headers

    response = requests.request("GET", url, headers=headers, params=querystring)

    data = response.json()

    try:
        for product in data['items']:
            soldout_product_list.append(product)
    except:
        print("No sold_out products found!")

def main():
    shopids = pd.read_csv('shopids.csv', index_col=0)
    max_shop_count = len(list(read_shop_list()))

    shop_list = []
    item_list = []
    inactive_shops = []

    for count, shop in enumerate(read_shop_list()):
        if count < 200:
            continue
        elif count >= 300:
            break
        try:
            # if count > 0 and count % MAX_SHOPS_PER_BROWSER == 0:
            #     create_new_browser_instance()

            print(f"\nScraping shop {count + 1} / {max_shop_count}")

            # shop_api = fetch_api(shop)

            shop_id = shopids.shopid[count]

            item_count = get_total_item_count(shop_id)

            print(f"Found {item_count} products for sale")

            for i in range(int(item_count / 100) + 1):
                get_product_listings(item_list, i, shop_id, inactive_shops)

            time.sleep(1)

            # soldout_item_count = get_total_soldout_item_count(shop_id)

            # print(f"Found {soldout_item_count} soldout products")

            # for i in range(int(soldout_item_count / 100) + 1):
            #     get_soldout_product_listings(soldout_item_list, i, shop_id)
        except:
            print(f"Error! Inspect shop {count} manually below")
            print(shop)

    shop_list_out = pd.json_normalize(shop_list)
    shop_list_out.to_csv('shops.csv')
    
    item_list_out = pd.json_normalize(item_list)
    item_list_out.to_csv('products.csv')

    # soldout_item_list_out = pd.json_normalize(soldout_item_list)
    # soldout_item_list_out.to_csv('soldout_products.csv')

    with open("inactive_shops.txt", "w") as output:
        for row in inactive_shops:
            output.write(str(row) + '\n')

if __name__ == "__main__":
    main()