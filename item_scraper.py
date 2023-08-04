from playwright.sync_api import sync_playwright
import pandas as pd

def read_csv():
    df = pd.read_csv('products.csv', usecols=['itemid', 'shopid', 'name'])
    csv = df.values.tolist()
    return csv

def check_scraped():
    try:
        df = pd.read_csv('test.csv', usecols=['url'])
        return df['url'].tolist()
    except:
        return []

def make_url(csv_count, csv_list):
    for i in range(csv_count):
        itemid = csv_list[i][0]
        shopid = csv_list[i][1]
        name = csv_list[i][2]
        name = name.replace(' ', '-')
        url = f"https://shopee.com.my/{name}-i.{shopid}.{itemid}"
        yield(url)

def main():
    csv_list = read_csv()
    csv_count = len(csv_list)
    categories_list = []
    url_list = []
    scraped_list = check_scraped()
    scraped_count = len(scraped_list)
    print(f"Found {scraped_count} already scraped.")

    for count, url in enumerate(make_url(csv_count, csv_list)):
        if url in scraped_list:
            continue
        if count > scraped_count + 4:
            break
        pw_url = url
        with sync_playwright() as pw:
            browser = pw.firefox.launch(headless=True)
            page = browser.new_page()
            page.goto(pw_url)
            print(f"\n{count + 1}. Getting {pw_url} categories..")
            page.locator('.shopee-button-outline.shopee-button-outline--primary-reverse').filter(has_text="English").click()
            page.wait_for_selector('a.akCPfg.KvmvO1')
            categories = page.locator('.akCPfg.KvmvO1')
            category_list = []
            for category in range(categories.count()):
                category_list.append(categories.nth(category).inner_text())
            print(f"Got {category_list}! [{count+1}/{len(csv_list)}]")
            categories_list.append(category_list)
            url_list.append(pw_url)

    category1_list, category2_list, category3_list, category4_list = [], [], [], []
    for category in categories_list:
        category1_list.append(category[0])
        category2_list.append(category[1])
        category3_list.append(category[2])
        category4_list.append(category[3])

    dict = {'url' : url_list, 'categories' : categories_list, 'category1' : category1_list, 'category2' : category2_list, 'category3' : category3_list, 'category4' : category4_list}

    out_df = pd.DataFrame(dict)

    if scraped_count == 0:
        out_df.to_csv('test.csv', mode='a')
    else:
        out_df.to_csv('test.csv', mode='a', header=False)        

if __name__ == "__main__":
    main()

