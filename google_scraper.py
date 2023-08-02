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

#Search term
def search(search_term):
	search_bar = driver.find_element(By.CLASS_NAME, 'gLFyf')
	search_bar.send_keys(search_term)

# Chrome options

chrome_options = Options()
chrome_options.add_argument('disable-notifications')
chrome_options.add_argument('--disable-infobars')
chrome_options.add_argument('start-maximized')
chrome_options.add_argument('disable-infobars')
# chrome_options.add_experimental_option("detach", True)

# Invoke browser and load site

# with open("google.html") as fp:
#     soup = BeautifulSoup(fp, 'html.parser')

driver = webdriver.Chrome(options=chrome_options)

driver.get('https://www.google.com/')

search('bicycle "online shop" site:shopee.com.my' + '\n')

time.sleep(15)

long_resulturl = f"{driver.current_url}&num=100"
url = str(long_resulturl)

driver.get(long_resulturl)

rows = []

time.sleep(2)

html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
soup = BeautifulSoup(html, "html.parser")

page_numbers = soup.find('table', class_='AaVjTc')
pages = page_numbers.find_all('a', {'class':'fl'})

for page in list(range(len(pages))):

	time.sleep(5)

	soup = BeautifulSoup(driver.page_source, "html.parser")

	wait = WebDriverWait(driver, 10)
	search_results = wait.until(EC.presence_of_element_located((By.ID, 'search')))

	try:
		for listing in soup.find_all('div', {'class': 'MjjYud'}):
		    #shop name
		    shop_name = listing.find('span', class_='dyjrff qzEoUe')
		    if shop_name is None:
		        name = ''
		    else:
		        name = shop_name.text
		        print(f"{page} - {name}")

		    #item list
		    item_link = listing.find('a', href=True)
		    if item_link is None:
		        link = ''
		    else:
		        link = item_link['href']

		    rows.append([name, link])

		start_listing_num=(page+1)*100

		print(f"scraping {page+1}")

		driver.get(f"{url}&start={start_listing_num}")

		time.sleep(5)

	except TimeoutException:
		print("Loading took too much time! - Try again")


for k,v in enumerate(rows,1):
    print(k,v)

with open('shopee_shop_list.csv','w', newline='',encoding='utf-8') as f:
	writer=csv.writer(f)
	writer.writerow(['name', 'link'])
	writer.writerows(rows)