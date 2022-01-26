import os, random, sys, time 
from selenium import webdriver
from bs4 import BeautifulSoup
import pickle
from datetime import date
from selenium.webdriver.chrome.options import Options
#------------------------------##------------------------------##------------------------------##------------------------------##------------------------------##------------------------------#

class wholefoods_scrape:
    path = (r"C:\Users\water\Desktop\WF\WholeFoods-Datascraping-Project-Deployment\Deployment\scraped products dump\list_of_items_" + str(date.today().strftime("%b_%d_%Y")) + ".pkl")
    def __init__(self,zipcode):
        self.zipcode = zipcode 
    def scraper(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')    
        try:
            browser = webdriver.Chrome('C:/Users/Water/Desktop/chromedriver.exe', options=options) # Chrome Driver
            browser.get('https://www.wholefoodsmarket.com/products/all-products?featured=on-sale') # Website Link
            browser.find_element_by_xpath("//input[@id='pie-store-finder-modal-search-field']").send_keys(self.zipcode) # Zip code
            time.sleep(3) # lag for 3 seconds to allow elements to load
            browser.find_elements_by_class_name("wfm-search-bar--list_item")[0].click()
        except:
            print('invalid zipcode')
        # Continously loads all possible product data until no more data exists
        # Sometimes may take some time if there are many products on sale
        try:
            load = browser.find_element_by_xpath("//span[contains(text(),'Load more')]") 
            while True:
                load.click()
                time.sleep(2.7) # Must have a 2 sec time lag so the 'load more' button can reappear
        except:
            print("Items on sale extracted, loading results...") # If all possible data is populated
        all_items = browser.find_elements_by_xpath("//div[@data-testid='product-tile']") # Pull all product elements by xpath
        list_of_items = [items.text.splitlines() for items in all_items] # Create a list comprehension of all product elements with text shown and lines split
        with open(path, 'wb') as handle:
            pickle.dump(list_of_items, handle, protocol=pickle.HIGHEST_PROTOCOL)
        print("Products saved as list_of_items_" + str(date.today().strftime("%b_%d_%Y")) + ".pkl")


#------------------------------##------------------------------##------------------------------##------------------------------##------------------------------##------------------------------#