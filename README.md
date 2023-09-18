# Shopee Scraper v2

# Introduction

This has been a major project of mine that came with a ton of hurdles that halted progress multiple times. This project is composed of multiple scripts that as a whole allowed me to obtain a comprehensive dataset containing details of a shop as well as details of the products that they have. This project has not been made for reusability (at least for now) as Shopee is a huge company that has a very talented workforce which constantly update their website. Over the course of 4 months I had to constantly change the approaches I had made to successfully get the end product. This is something I do not wish to do repeatedly as it took an exhaustive amount of effort. However, I am currently working on an alternative solution that I believe could be reused in a clean and safe manner, albeit maybe only being ~90% accurate (Stay tuned!) (Maybe if I'm not lazy!). 

# Briefly how it works
1. Based on a target keyword, links of shops in shopee that specialize in selling the keyword is scraped with the google scraper.
2. Each link is visited and APIs are tapped to get both details of the shop and their products. Both are stored into separate CSV files for later use. Product data however isn't fully comprehensive and doesn't have target features such as "subcategories" which I am in need of. Luckily there is another source for product details. If however, product data from here is sufficient, there is no need to proceed below. All this is done with the shopee scraper.
3. The product API is needed to be used, this API provides all the details of only one specific product at a time and is generally used for display on the product's webpage. ProductIDs from the product CSV file obtained from step 2 is fed into the Item Scraper to get full details of the products. Output is saved in a clean and curated CSV file.

## Google Scraper
## Shopee Scraper
## Item Scraper

# Conclusion
Overall satisfied with the data obtained from this project. Using the keyword "Bicycle" netted me 274 Shops and around 70k unique products total. Shops however, especially in Shopee, have several unsold but listed products in their listings. Analysis of what was sold in a month showed what ended up only being about 7k unique products. Due to the fact that shops in Shopee can sell relatively whatever they want, certain shops may sell multiple things other than your target keyword. Therefore, further data cleaning is needed to obtain a purer dataset as all products are scraped from the shops.
