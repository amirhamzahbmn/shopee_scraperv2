from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
import time
import csv

#Access shadowRoot of an element
def expand_element(element): 
	return driver.execute_script("return arguments[0].shadowRoot", element)

def get_shop_description():
    soup = BeautifulSoup(driver.page_source, "html.parser")
    #Name, Active/Holiday mode
    try:
        shop_name = soup.find('h1', class_='section-seller-overview-horizontal__portrait-name')
        if shop_name is None:
            shop_name = ''
        else:
            shop_name = shop_name.text
        active_time = soup.find('div', class_='section-seller-overview-horizontal__active-time')
        if active_time is None:
            active_time = ''
        else:
            active_time = active_time.text
        holiday_status = soup.find('div', class_='section-seller-overview-horizontal__holiday-mode')
        if holiday_status is None:
            holiday_status = ''
        else:
            holiday_status = holiday_status.text

        shop_description.append([shop_name, active_time, holiday_status])


    except TimeoutException:
        print("Loading took too much time! - Try again")

    #Products, Followers, Following, Rating, Chat performance, Joined
    try:
        for category in soup.find('div', class_='section-seller-overview-horizontal__seller-info-list'):
            value = category.find('div', class_='section-seller-overview__item-text-value')
            if value is None:
                value = ''
            else:
                shop_description[-1].append(value.text)
            
    except TimeoutException:
        print("Loading took too much time! - Try again")


def get_product_data():

    soup = BeautifulSoup(driver.page_source, "html.parser")

    try:
        #shop name
        shop_name = soup.find('h1', class_='section-seller-overview-horizontal__portrait-name')
        if shop_name is None:
            shop_name = ''
        else:
            shop_name = shop_name.text
        #listings
        for item in soup.find_all('div', {'class': 'shop-search-result-view__item col-xs-2-4'}):
            #item name
            item_n = item.find('div', class_='+ANuoG _3y98Gb XfZXsZ')
            if item_n is None:
                name = ''
            else:
                name = item_n.text

            #item initial cost
            item_init_c = item.find('div', class_='ykhwOa UwF8NE GQ3Ris')
            if item_init_c is None:
                init_cost = ''
            else:
                init_cost = item_init_c.text

            #item cost
            item_c = item.find_all('span', class_='Hftxcn')
            if item_c is None:
                cost = ''
            elif len(item_c) > 1:
                cost = f"{item_c[0].text} - {item_c[1].text}"
            else:
                cost = item_c[0].text

            #discount percentage
            item_dp = item.find('span', class_='percent')
            if item_dp is None:
                disc_percent = ''
            else:
                disc_percent = item_dp.text

            #item sales amount
            item_s = item.find('div', class_='YSpAGT m70u+x')
            if item_s is None:
                sales = ''
            else:
                sales = item_s.text

            #if local_seller
            item_l = item.find('div', class_='U1mug-')
            if item_l is None:
                location = ''
            else:
                location = item_l.text

            #item link
            item_link = item.find('a', href=True)
            if item_link is None:
                link = ''
            else:
                link = f"https://shopee.com.my{item_link['href']}"

            products.append([shop_name, name, init_cost, cost, disc_percent, sales, location, link])

    except TimeoutException:
        print("Loading took too much time! - Try again")

# Chrome options

chrome_options = Options()
chrome_options.add_argument('disable-notifications')
chrome_options.add_argument('--disable-infobars')
chrome_options.add_argument('start-maximized')
chrome_options.add_argument('disable-infobars')
#Enable when need to check source code
chrome_options.add_experimental_option("detach", True)

# #Close Popups
# # Wait for the language prompt to appear and click it
# wait = WebDriverWait(driver, 7)
# language_prompt = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/div[1]/div/div[3]/div[1]/button')))
# language_prompt.click()

# Search term and sort by top_sales

shop_description = []
products = []

shop_list_file = "shopee_shop_list.csv"
shop_list = []
with open(shop_list_file, 'r') as file:
    csvreader = csv.reader(file)
    header = next(csvreader)
    for row in csvreader:
        shop_list.append(row[1])

driver = webdriver.Chrome(options=chrome_options)

for i,shop in enumerate(shop_list):
    driver.get(shop)
    time.sleep(2)

    if i == 0:
        wait = WebDriverWait(driver, 7)
        #popup english language button
        language_prompt = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="modal"]/div[1]/div[1]/div/div[3]/div[1]/button')))
        language_prompt.click()

    soup = BeautifulSoup(driver.page_source, "html.parser")

    get_shop_description()

    max_page = soup.find('span', 'shopee-mini-page-controller__total')
    for i in list(range(6)):
        ActionChains(driver).scroll_by_amount(0,1000).perform()
        time.sleep(0.5)

    if max_page is None:
        continue

    for i in range(int(max_page.text)):
        get_product_data()
        nxt_button = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div/div/div/div[2]/div/div[3]/div[2]/div[2]/div/div[1]/div[2]/button[2]')
        nxt_button.click()
        time.sleep(2)

with open('shopee_shop_descriptions.csv','w', newline='',encoding='utf-8') as f:
  writer=csv.writer(f)
  writer.writerow(['shop_name','last_active_time','holiday_status','product_amt','follower_amt','following_amt','shop_rating','shop_chat_performance','joined_date'])
  writer.writerows(shop_description)

with open('shopee_shop_products.csv','w', newline='',encoding='utf-8') as f:
  writer=csv.writer(f)
  writer.writerow(['shop_name','name','initial_cost','cost','discount','sales_amt','local_seller','link'])
  writer.writerows(products)

# for k,v in enumerate(products):
#     print(k,v)

# for term in search_terms:
#     print(f"\nscraping data for {term}...")
#     url = get_url(term)

#     # Invoke browser and load site

#     for page in range(0,max_pages):
#         driver.get(url.format(page))
#         time.sleep(1)

#         if page == 0:
#             wait = WebDriverWait(driver, 7)
#             #popup english language button
#             language_prompt = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="modal"]/div[1]/div[1]/div/div[3]/div[1]/button')))
#             language_prompt.click()
#             print("scrolling page..")
#             get_data()
#             print(f"scraped page {page+1}/{max_pages}")
#         else:
#             print("scrolling page..")
#             get_data()
#             print(f"scraped page {page+1}/{max_pages}")
        
#     print(f'\nall "{term}" data has been scraped.')

# # for k,v in enumerate(rows,1):
# #     print(k,v)

# with open('shopee_item_list.csv','w', newline='',encoding='utf-8') as f:
# 	writer=csv.writer(f)
# 	writer.writerow(['search_term', 'name', 'init_cost', 'cost', 'disc_percent', 'sales', 'location', 'link'])
# 	writer.writerows(rows)

# print("\nall done! data is stored in a CSV file in your directory.")