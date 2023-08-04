import polars as pl
import pandas as pd
import requests
import random
import sys
from time import sleep

url = "https://shopee.com.my/api/v4/pdp/get_pc"

headers = {
    "cookie": "__LOCALE__null=MY; _gcl_au=1.1.13925975.1690518921; csrftoken=A8MTdmAzaYIuCXVtVD2DP7pEqRiutZG5; SPC_T_IV=Q2Z0dEJHczZsakVMNmJTcg==; SPC_F=XX8blyffS3buCBuCz3je4ZUCLAds4psj; REC_T_ID=29b9d988-2d00-11ee-9430-2cea7f960de8; SPC_R_T_ID=W20ypQmGQa97d7RhqO2YNLHreEwg5BorthA5DrYtYzbNSzqtYvk2pjpeLs90cOHSMm8F5jvbQWlhGuy/1+hxb/l0ETDfqOlos0CxLYZmiYfqU9Zdids7irfJcv05RB/k6qnyJv8GfheFOmPMZ4vNaczy4MeSa1acKQ681U+DlM8=; SPC_R_T_IV=Q2Z0dEJHczZsakVMNmJTcg==; SPC_T_ID=W20ypQmGQa97d7RhqO2YNLHreEwg5BorthA5DrYtYzbNSzqtYvk2pjpeLs90cOHSMm8F5jvbQWlhGuy/1+hxb/l0ETDfqOlos0CxLYZmiYfqU9Zdids7irfJcv05RB/k6qnyJv8GfheFOmPMZ4vNaczy4MeSa1acKQ681U+DlM8=; SPC_SI=EHu/ZAAAAAAwTnEyeXpLbTyGIgAAAAAAWGxSdTFhb00=; _fbp=fb.2.1690518922399.331916392; _QPWSDCXHZQA=8d3f86e2-721b-4c8e-dafb-837fda72845d; AMP_TOKEN=%24NOT_FOUND; _gid=GA1.3.2074780246.1690518927; language=en; _med=refer; shopee_webUnique_ccd=aL14tzSIUkRqdoLHcYcq3Q%3D%3D%7CkY%2FsXR80en1oKd4AQhesocOa6mBlwEy%2FGIdY3V2eOzpuS49c8yEjrq6XGHH6X5bLpOkDEtSO%2FPlA07k%3D%7CWgdAs%2FdUDaNNDKSA%7C08%7C3; ds=08d032326a7eead074969450b48bed40; _ga=GA1.1.1160021187.1690518927; _dc_gtm_UA-61915055-6=1; _ga_NEYMG30JL4=GS1.1.1690518927.1.1.1690520692.0.0.0",
    "5d9ee93": ")&E5VQb&u+qdF\\3%\u0021b)HapB7]",
    "70a9407d": "gDdBN$1Ah8))\u0021*u\u0021K1d@o5m;e",
    "8441355d": """S(*k@@1<N4GROmJhR&L3rn1tfOA('d('@G0*?CI<)e-#E_Y@sP^W_X$W8Dbbi@n)#pP0Xbi9cHODbKC%=#C(8ag3UfmTM%b7nIe[0)Cneea]UGjEulh<@rD9X:*I@N%&.V,Kmf]R=NC1"2Wo+Er5=Nc<_ZRlCl9?Y\u0021-/6$^/NZi133`(A9ri5^+>g:sepS<4$ZL$`Le;X%pM$Q[=GE/h]Jj?/RO8i3N(9N*R-=b6*<V/EP*k$KNGn[2.I2AO&m_(\u0021_4AFRGE/BgmfE:*s)7ck\u0021mT"/6WRi;,f\\U5\\\\j*MNTd0.EY62e],/2*M<;TF&`gDlu]/O$?P91n:D8jQ&Z%YH+7iR:9j)?R(BM-#18D+8A"q""",
    "authority": "shopee.com.my",
    "accept": "application/json",
    "accept-language": "en-US,en;q=0.9",
    "af-ac-enc-dat": "AAcyLjkuMi0yAAABiZrijGMAABCkAzAAAAAAAAAAAj+vsCOmPFyU/ytSpbZSLToKuPUCae7h0EtR98m34Z0aGIbus0Lz9m1hJq2ZN8bK8jmG+cm3ncZ8zlzi5R3AI97TTLd03piD6Oej+hMsBxDkOFXuaQLso9VhpO1qzeliuGLH0reJvJHuk7Jc641ka0YFC7m8Xk1TyedShJ7FB+nk0K4kHoQP2ej9N6E663snAmTlP2ftzoAHKX+I31z8KKr7bebmANXKcEZn7YxaKzb/TT7B3udf1mpviLxpue1fzPQawxhkDVFVAI9GEIwQ2b6pSC2AoZP1OHtQrKs+DBy9cy+asoYfCSZDomGd2N/f6JxtxXN9MrqfgHMbmHinxYoLOBwyvkYGEv+kG51AXrU3R+t+AezbDk/V38SD/aE9vt3GXc52ZPiAN3liYqVPOmJbpMxgRATDD/1szNzL+OeGJNaFO5f/NhMnw8f21UXD2mkb2Js4fgyhyOmWOwejDo7KtGV7N+1hvhVdRaZwLolYuklTPvBqrt9wFMZrUTO6s3R08nV3F2dEcsHrrQKFakVzWq/3pjTJzgNsDfkvZHtJElri+gf9BJ5rmlzPMgc1VDQc2z4AdhoxDgLO3UkVN+cFQVlliwNIwJqikhcFaxcNjyV9Ewf9BJ5rmlzPMgc1VDQc2z4zna7JPsRP4UQ6h1PWalt6bdGHPnfHtEc9RYVqSekoRczoUhKAg6vJXYPkXE5ho+pc0XG8frvsLhQK78fs7wwwyC7rKfNc6s44ecEdNCy+XYAdcThqjezyG/eDtPLFUjBc0XG8frvsLhQK78fs7wwwmomcVeHSHfGU2yXdbB6xTbfEmLpJoIJZrwE8rkVLntf6puWUDCNQnWs1gQSFkyS0E5H7Y3eRdD+uDxvh698/xREOPwNtVPYJNjimHZDfD9KX/zYTJ8PH9tVFw9ppG9ibl/82EyfDx/bVRcPaaRvYmzaowmTYQ1AQ0fs+1rOtegEdnkNe+iRpQibJYxnnp5zoCInEqQK0azi6aFC4fInOtaFHLrjI3cERD4ApHR+Y9ffIgtm85Z6eK/q5Uso7+swA0RySdhyhKzToeXrsCr/7Vv/R+G2cAxuc5Jr8Jg6j/hU=",
    "af-ac-enc-sz-token": "aL14tzSIUkRqdoLHcYcq3Q==|kY/sXR80en1oKd4AQhesocOa6mBlwEy/GIdY3V2eOzpuS49c8yEjrq6XGHH6X5bLpOkDEtSO/PlA07k=|WgdAs/dUDaNNDKSA|08|3",
    "content-type": "application/json",
    "referer": "https://shopee.com.my/",
    "sec-ch-ua": '"Not/A)Brand";v="99", "Microsoft Edge";v="115", "Chromium";v="115"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Linux"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "sz-token": "aL14tzSIUkRqdoLHcYcq3Q==|kY/sXR80en1oKd4AQhesocOa6mBlwEy/GIdY3V2eOzpuS49c8yEjrq6XGHH6X5bLpOkDEtSO/PlA07k=|WgdAs/dUDaNNDKSA|08|3",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.188",
    "x-api-source": "pc",
    "x-csrftoken": "A8MTdmAzaYIuCXVtVD2DP7pEqRiutZG5",
    "x-requested-with": "XMLHttpRequest",
    "x-sap-ri": "754cc364b17de8b80024d2325656056c894a3555a07f3b9b",
    "x-shopee-language": "en",
    "x-sz-sdk-version": "2.9.2-2&1.4.1"
}

keys = ['item_id',
 'shop_id',
 'user_id',
 'price_max_before_discount',
 'has_lowest_price_guarantee',
 'price_before_discount',
 'price_min_before_discount',
 'exclusive_price_info',
 'price_min',
 'price_max',
 'price',
 'stock',
 'discount',
 'historical_sold',
 'sold',
 'show_discount',
 'raw_discount',
 'name',
 'ctime',
 'item_status',
 'status',
 'condition',
 'catid',
 'description',
 'is_mart',
 'show_shopee_verified_label',
 'reference_item_id',
 'brand',
 'liked',
 'liked_count',
 'cmt_count',
 'shopee_verified',
 'is_adult',
 'is_preferred_plus_seller',
 'bundle_deal_id',
 'can_use_bundle_deal',
 'can_use_wholesale',
 'item_type',
 'is_official_shop',
 'shop_location',
 'cb_option',
 'is_pre_order',
 'estimated_days',
 'show_free_shipping',
 'cod_flag',
 'is_service_by_shopee',
 'show_original_guarantee',
 'other_stock',
 'item_has_post',
 'discount_stock',
 'current_promotion_has_reserve_stock',
 'current_promotion_reserved_stock',
 'normal_stock',
 'brand_id',
 'show_recycling_info',
 'show_best_price_guarantee',
 'item_has_video',
 'item_has_size_recommendation',
 'is_cc_installment_payment_eligible',
 'is_non_cc_installment_payment_eligible',
 'has_low_fulfillment_rate',
 'is_partial_fulfilled',
 ]

WRITE_COUNT = 20000

def write_to_csv():
    print(f"Writing into csv..")
    with open("item_products.csv", mode="ab") as f:
        df.write_csv(f, has_header=False)

try:
    productids = pd.read_csv('productids.csv')
    productid_list = productids.values.tolist()
except:
    try:
        print("Product ids not found, will generate a new productids.csv")
        productids = pd.read_csv('products.csv', usecols=['itemid','shopid'])
        productids.to_csv('productids.csv', index=False)
        productid_list = productids.values.tolist()
    except:
        print("No products file found, output from shopee_scraper.py must be in the same folder!")
        sys.exit("Exiting.")

try:
    scanned_products_df = pl.read_csv('item_products.csv', columns=['item_id'], null_values='null')
    scanned_products_list = scanned_products_df['item_id'].to_list()
    print(f"found {len(scanned_products_list)} scanned.")
except:
    print("No scanned products found, will generate new csv file.")
    scanned_products_list = []

df = pl.read_csv('products_template.csv')

for count, id in enumerate(productid_list):
    if id[0] in scanned_products_list:
        continue
    if id[0] == 'null':
        continue
    if count == len(scanned_products_list) + WRITE_COUNT + 1:
        break
    if count % 100 == 0:
        write_to_csv()
        df = df.clear()

    querystring = {"shop_id":id[1],"item_id":id[0]}

    response = requests.request("GET", url, headers=headers, params=querystring)
    json = response.json()
    data = json['data']['item']

    data_dict = {}
    for key in keys:
        try:
            data_dict[key] = str(data[key])
        except:
            data_dict[key] = 'null'

    separator = ';'
    separator2 = ','
    
    try:
        data_dict['categories'] = separator.join(category['display_name'] for category in data['categories'])
    except:
        data_dict['categories'] = 'null'
    try:
        data_dict['fe_categories'] = separator.join(fe_category['display_name'] for fe_category in data['fe_categories'])
    except:
        data_dict['fe_categories'] = 'null'
    try:
        data_dict['shop_vouchers'] = separator.join(f"{voucher['voucher_code']} - {voucher['discount_value']/100000} off min spend {voucher['min_spend']/100000}" for voucher in data['shop_vouchers'])
    except:
        data_dict['shop_vouchers'] = 'null'
    try:
        data_dict['wholesale_tier_list'] = separator.join(f"{tier['min_count']} <= {tier['max_count']} = {tier['price']/100000}" for tier in data['wholesale_tier_list'])
    except:
        data_dict['wholesale_tier_list'] = 'null'
    try:
        data_dict['models'] = separator.join(f"{model['name']} - price : {model['price']/100000} from {model['price_before_discount']/100000}, stock : {model['stock']}" for model in data['models'])
    except:
        data_dict['models'] = 'null'
    try:
        data_dict['tier_variations'] = separator.join(f"{variation['name']} - {separator2.join(option for option in variation['options'])}" for variation in data['tier_variations'])
    except:
        data_dict['tier_variations'] = 'null'
    try:
        data_dict['attributes'] = separator.join(f"{attribute['name']} - {attribute['value']}" for attribute in data['attributes'])
    except:
        data_dict['attributes'] = 'null'
    try:
        data_dict['rating_star'] = str(data['item_rating']['rating_star'])
    except:
        data_dict['rating_star'] = 'null'
    try:
        data_dict['rating_count'] = separator.join(str(rating) for rating in data['item_rating']['rating_count'])
    except:
        data_dict['rating_count'] = 'null'

    df_pulled = pl.from_dict(data_dict)
    df.extend(df_pulled)

    print(f"{count}. {id[1]} - {id[0]}")
    sleeptime = random.uniform(0.5, 1)
    sleep(sleeptime)

write_to_csv()
