import os, random, sys, time 
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
try:
    browser = webdriver.Chrome('C:/Users/Water/Desktop/chromedriver.exe', options=options) # Chrome Driver
    browser.get('https://www.wholefoodsmarket.com/products/all-products?featured=on-sale') # Website Link
    print('Please enter your zipcode to find sales at a store near you...')
    browser.find_element_by_xpath("//input[@id='pie-store-finder-modal-search-field']").send_keys(input()) # Zip code
    time.sleep(2.5) # lag for 3 seconds to allow elements to load
    browser.find_elements_by_class_name("wfm-search-bar--list_item")[0].click()
except:
    print('invalid zipcode')
time.sleep(2)

browser.get('https://www.wholefoodsmarket.com/products/produce?featured=on-sale') # Website Link
#---------------------
# Continously loads all possible product data until no more data exists
# Sometimes may take some time if there are many products on sale
try:
    load = browser.find_element_by_xpath("//span[contains(text(),'Load more')]") 
    while True:
        load.click()
        time.sleep(2.5) # Must have a 2 sec time lag so the 'load more' button can reappear
except:
    print("Results Filled") # If all possible data is populated
all_items = browser.find_elements_by_xpath("//div[@data-testid='product-tile']") # Pull all product elements by xpath
produce = [items.text.splitlines() for items in all_items] # Create a list comprehension of all product elements with text shown and lines split

browser.get('https://www.wholefoodsmarket.com/products/dairy-eggs?featured=on-sale')
try:
    load = browser.find_element_by_xpath("//span[contains(text(),'Load more')]") 
    while True:
        load.click()
        time.sleep(2.5) # Must have a 2 sec time lag so the 'load more' button can reappear
except:
    print("Results Filled") # If all possible data is populated
all_items = browser.find_elements_by_xpath("//div[@data-testid='product-tile']") # Pull all product elements by xpath
dairy_eggs = [items.text.splitlines() for items in all_items] # Create a list comprehension of all product elements with text shown and lines split

browser.get('https://www.wholefoodsmarket.com/products/meat?featured=on-sale')
try:
    load = browser.find_element_by_xpath("//span[contains(text(),'Load more')]") 
    while True:
        load.click()
        time.sleep(2.5) # Must have a 2 sec time lag so the 'load more' button can reappear
except:
    print("Results Filled") # If all possible data is populated
all_items = browser.find_elements_by_xpath("//div[@data-testid='product-tile']") # Pull all product elements by xpath
meat = [items.text.splitlines() for items in all_items] # Create a list comprehension of all product elements with text shown and lines split

browser.get('https://www.wholefoodsmarket.com/products/prepared-foods?featured=on-sale')
try:
    load = browser.find_element_by_xpath("//span[contains(text(),'Load more')]") 
    while True:
        load.click()
        time.sleep(2.5) # Must have a 2 sec time lag so the 'load more' button can reappear
except:
    print("Results Filled") # If all possible data is populated
all_items = browser.find_elements_by_xpath("//div[@data-testid='product-tile']") # Pull all product elements by xpath
prepared_foods = [items.text.splitlines() for items in all_items] # Create a list comprehension of all product elements with text shown and lines split

browser.get('https://www.wholefoodsmarket.com/products/pantry-essentials?featured=on-sale')
try:
    load = browser.find_element_by_xpath("//span[contains(text(),'Load more')]") 
    while True:
        load.click()
        time.sleep(2.5) # Must have a 2 sec time lag so the 'load more' button can reappear
except:
    print("Results Filled") # If all possible data is populated
all_items = browser.find_elements_by_xpath("//div[@data-testid='product-tile']") # Pull all product elements by xpath
pantry_essentials = [items.text.splitlines() for items in all_items] # Create a list comprehension of all product elements with text shown and lines split

browser.get('https://www.wholefoodsmarket.com/products/breads-rolls-bakery?featured=on-sale')
try:
    load = browser.find_element_by_xpath("//span[contains(text(),'Load more')]") 
    while True:
        load.click()
        time.sleep(2.5) # Must have a 2 sec time lag so the 'load more' button can reappear
except:
    print("Results Filled") # If all possible data is populated
all_items = browser.find_elements_by_xpath("//div[@data-testid='product-tile']") # Pull all product elements by xpath
bread_rolls_bakery = [items.text.splitlines() for items in all_items] # Create a list comprehension of all product elements with text shown and lines split

browser.get('https://www.wholefoodsmarket.com/products/desserts?featured=on-sale')
try:
    load = browser.find_element_by_xpath("//span[contains(text(),'Load more')]") 
    while True:
        load.click()
        time.sleep(2.5) # Must have a 2 sec time lag so the 'load more' button can reappear
except:
    print("Results Filled") # If all possible data is populated
all_items = browser.find_elements_by_xpath("//div[@data-testid='product-tile']") # Pull all product elements by xpath
desserts = [items.text.splitlines() for items in all_items] # Create a list comprehension of all product elements with text shown and lines split

browser.get('https://www.wholefoodsmarket.com/products/body-care?featured=on-sale')
try:
    load = browser.find_element_by_xpath("//span[contains(text(),'Load more')]") 
    while True:
        load.click()
        time.sleep(2.5) # Must have a 2 sec time lag so the 'load more' button can reappear
except:
    print("Results Filled") # If all possible data is populated
all_items = browser.find_elements_by_xpath("//div[@data-testid='product-tile']") # Pull all product elements by xpath
body_care = [items.text.splitlines() for items in all_items] # Create a list comprehension of all product elements with text shown and lines split

browser.get('https://www.wholefoodsmarket.com/products/supplements?featured=on-sale')
try:
    load = browser.find_element_by_xpath("//span[contains(text(),'Load more')]") 
    while True:
        load.click()
        time.sleep(2.5) # Must have a 2 sec time lag so the 'load more' button can reappear
except:
    print("Results Filled") # If all possible data is populated
all_items = browser.find_elements_by_xpath("//div[@data-testid='product-tile']") # Pull all product elements by xpath
supplements = [items.text.splitlines() for items in all_items] # Create a list comprehension of all product elements with text shown and lines split

browser.get('https://www.wholefoodsmarket.com/products/frozen-foods?featured=on-sale')
try:
    load = browser.find_element_by_xpath("//span[contains(text(),'Load more')]") 
    while True:
        load.click()
        time.sleep(2.5) # Must have a 2 sec time lag so the 'load more' button can reappear
except:
    print("Results Filled") # If all possible data is populated
all_items = browser.find_elements_by_xpath("//div[@data-testid='product-tile']") # Pull all product elements by xpath
frozen_foods = [items.text.splitlines() for items in all_items] # Create a list comprehension of all product elements with text shown and lines split

browser.get('https://www.wholefoodsmarket.com/products/snacks-chips-salsas-dips?featured=on-sale')
try:
    load = browser.find_element_by_xpath("//span[contains(text(),'Load more')]") 
    while True:
        load.click()
        time.sleep(2.5) # Must have a 2 sec time lag so the 'load more' button can reappear
except:
    print("Results Filled") # If all possible data is populated
all_items = browser.find_elements_by_xpath("//div[@data-testid='product-tile']") # Pull all product elements by xpath
snacks_chips_salsas_dips = [items.text.splitlines() for items in all_items] # Create a list comprehension of all product elements with text shown and lines split

browser.get('https://www.wholefoodsmarket.com/products/seafood?featured=on-sale')
try:
    load = browser.find_element_by_xpath("//span[contains(text(),'Load more')]") 
    while True:
        load.click()
        time.sleep(2.5) # Must have a 2 sec time lag so the 'load more' button can reappear
except:
    print("Results Filled") # If all possible data is populated
all_items = browser.find_elements_by_xpath("//div[@data-testid='product-tile']") # Pull all product elements by xpath
seafood = [items.text.splitlines() for items in all_items] # Create a list comprehension of all product elements with text shown and lines split

browser.get('https://www.wholefoodsmarket.com/products/beverages?featured=on-sale')
try:
    load = browser.find_element_by_xpath("//span[contains(text(),'Load more')]") 
    while True:
        load.click()
        time.sleep(2.5) # Must have a 2 sec time lag so the 'load more' button can reappear
except:
    print("Results Filled") # If all possible data is populated
all_items = browser.find_elements_by_xpath("//div[@data-testid='product-tile']") # Pull all product elements by xpath
Beverages = [items.text.splitlines() for items in all_items] # Create a list comprehension of all product elements with text shown and lines split

browser.get('https://www.wholefoodsmarket.com/products/beauty?featured=on-sale')
try:
    load = browser.find_element_by_xpath("//span[contains(text(),'Load more')]") 
    while True:
        load.click()
        time.sleep(2.5) # Must have a 2 sec time lag so the 'load more' button can reappear
except:
    print("Results Filled") # If all possible data is populated
all_items = browser.find_elements_by_xpath("//div[@data-testid='product-tile']") # Pull all product elements by xpath
beauty = [items.text.splitlines() for items in all_items] # Create a list comprehension of all product elements with text shown and lines split

browser.get('https://www.wholefoodsmarket.com/products/floral?featured=on-sale')
try:
    load = browser.find_element_by_xpath("//span[contains(text(),'Load more')]") 
    while True:
        load.click()
        time.sleep(2.5) # Must have a 2 sec time lag so the 'load more' button can reappear
except:
    print("Results Filled") # If all possible data is populated
all_items = browser.find_elements_by_xpath("//div[@data-testid='product-tile']") # Pull all product elements by xpath
floral = [items.text.splitlines() for items in all_items] # Create a list comprehension of all product elements with text shown and lines split

browser.get('https://www.wholefoodsmarket.com/products/lifestyle?featured=on-sale')
try:
    load = browser.find_element_by_xpath("//span[contains(text(),'Load more')]") 
    while True:
        load.click()
        time.sleep(2.5) # Must have a 2 sec time lag so the 'load more' button can reappear
except:
    print("Results Filled") # If all possible data is populated
all_items = browser.find_elements_by_xpath("//div[@data-testid='product-tile']") # Pull all product elements by xpath
lifestyle = [items.text.splitlines() for items in all_items] # Create a list comprehension of all product elements with text shown and lines split
print('There are ' + str(len(lifestyle) + len(produce) + len(dairy_eggs) + len(meat) + len(prepared_foods) + len(pantry_essentials) + len(bread_rolls_bakery) + len(desserts) + len(body_care) + len(supplements) + len(frozen_foods) + len(snacks_chips_salsas_dips) + len(seafood) + len(Beverages) + len(beauty) + len(floral)) + ' products on sale queried.')
list_of_categories = ['lifestyle', 'produce', 'dairy_eggs', 'meat', 'prepared_foods', 'pantry_essentials', 'bread_rolls_bakery', 'desserts', 'body_care', 'supplements', 'frozen_foods', 'snacks_chips_salsas_dips', 'seafood', 'Beverages', 'beauty', 'floral']

d = {"company":[], "product":[], "regular":[], "sale":[], "prime":[], "category":[]} # Create a Dict


for category in list_of_categories:
    for i in range(len(globals()[category])):                        # At the range of the length of all items (will loop i times)
            d["company"].append(globals()[category][i][-5])      # Append respective indexed data in list_of_items[i] for each column
            d["product"].append(globals()[category][i][-4])      # | -
            d["regular"].append(globals()[category][i][-3][8:])  # | * 
            d["sale"].append(globals()[category][i][-2][10:])    # | /
            d["prime"].append(globals()[category][i][-1][18:])
            d["category"].append(str(category))   # | \
#------------------------------------------------------# | /
if len(d['company']) == len(d['product']) == len(d['regular']) == len(d['sale']) == len(d['category']):  # Verify that the length of each column is == to each other, otherwise the dataframe wont be populated   
    print("All column lengths are equal, there are " + str(len(d['company'])) + " products on sale today.")
else:                                                  # | \        
    print("Error, column lengths are not equal.")      # | /
pd.set_option("display.max_rows", 500)                 # | \ Change Pandas option to view more rows of the df
df = pd.DataFrame.from_dict(d)                         # | / Turn our Dict to a Pandas DataFrame  


if df['product'].str.contains('Original Vegan Bagels, 15.87 oz').any():                         
    ix = df[df['product'].str.contains('Original Vegan Bagels, 15.87 oz')].index
    for i in range(len(ix)):
        df.loc[ix[i],'company'] = "Soozy's"

if df['product'].str.contains('Original Sandwich Bread, 22.2 oz').any():                         
    ix = df[df['product'].str.contains('Original Sandwich Bread, 22.2 oz')].index
    for i in range(len(ix)):
        df.loc[ix[i],'company'] = "Soozy's"

if df['product'].str.contains('Arctic Char Fillet').any():                         
    ix = df[df['product'].str.contains('Arctic Char Fillet')].index
    for i in range(len(ix)):
        df.loc[ix[i],'company'] = "Whole Foods Market"

# Data cleaning/shifting for products by Brita
if df['company'].str.contains('/').any() and df['product'].str.contains('Brita').any():
    print('data error check company name containing "/" and "Brita"')

# Data cleaning/shifting for products
if df['product'].str.contains("Easy Peel White Shrimp 8-12 Count").any():
    ix = df[df['product'].str.contains("Easy Peel White Shrimp 8-12 Count")].index
    for i in range(len(ix)):
        df.loc[ix[i],'company'] = "Whole Foods Market"

if df['product'].str.contains("Organic Freeze Dried Chives, 0.14 oz").any():
    ix = df[df['product'].str.contains("Organic Freeze Dried Chives, 0.14 oz")].index
    for i in range(len(ix)):
        df.loc[ix[i],'company'] = "Green Garden"

if df['product'].str.contains("Organic Freeze Dried Thyme, 0.26 oz").any():
    ix = df[df['product'].str.contains("Organic Freeze Dried Thyme, 0.26 oz")].index
    for i in range(len(ix)):
        df.loc[ix[i],'company'] = "Green Garden"

if df['product'].str.contains("Organic Mild Plant Taco Meatless Crumbles").any():
    ix = df[df['product'].str.contains("Organic Mild Plant Taco Meatless Crumbles")].index
    for i in range(len(ix)):
        df.loc[ix[i],'company'] = "PLANT BOSS"

if df['product'].str.contains("Organic Multicolor Kale").any():
    ix = df[df['product'].str.contains("Organic Multicolor Kale")].index
    for i in range(len(ix)):
        df.loc[ix[i],'company'] = "Whole Foods Market"        

# Data cleaning/shifting for products by Soozy's
if df['product'].str.contains("Soozy's Birthday Cake Cookies").any():
    ix = df[df['product'].str.contains("Soozy's Birthday Cake Cookies")].index
    for i in range(len(ix)):
        df.loc[ix[i],'company'] = "Soozy's"

if df['product'].str.contains("Soozys Chocolate Chip Cookies").any():
    ix = df[df['product'].str.contains("Soozys Chocolate Chip Cookies")].index
    for i in range(len(ix)):
        df.loc[ix[i],'company'] = "Soozy's"

# Data cleaning/shifting for products by Whole Foods Market
if df['product'].str.contains('Whole Foods Market').any():
    print('data error check product name containing "whole foods market"')

#---------------Any of these are definitely under the lifestyle category//all waterbottles------#

# Data cleaning/shifting for products by CAMELBAK
if df['product'].str.contains('CAMELBAK').any():
    print('data error check product name containing "CAMELBAK"')

# Data cleaning/shifting for products by NEW WAVE
if df['product'].str.contains('NEW WAVE').any():
    print('data error check product name containing "NEW WAVE"')

# Data cleaning/shifting for products by Enviro
if df['product'].str.contains('Enviro').any():
    print('data error check product name containing "Enviro"')

# Data cleaning/shifting for products by HYDRO FLASK
if df['product'].str.contains('HYDRO FLASK').any():
    print('data error check product name containing "HYDRO FLASK"')

# Data cleaning/shifting for products by SUNDESA
if df['product'].str.contains('SUNDESA').any():
    print('data error check product name containing "SUNDESA"')

if df['regular'].str.contains('9¢').any():
    ix = df[df['regular'].str.contains('9¢')].index
    for i in range(len(ix)):
        df.loc[ix[i], 'regular'] = '9' + df.loc[ix[i], 'regular']

if df['company'].str.contains('365').any():
    ix = df[df['company'].str.contains('365')].index
    for i in range(len(ix)):
        df.loc[ix[i], 'company'] = 'Whole Foods Market'

df['sale'] = df['sale'].str.replace(r'$', '', regex=True)
df['prime'] = df['prime'].str.replace(r'$', '', regex=True)
df['regular'] = df['regular'].str.replace(r'$', '', regex=True)

if df['regular'].str.contains('/lb').any():
    ix = df[df['regular'].str.contains('/lb')].index
    for i in range(len(ix)):
        df.loc[ix[i], 'regular'] = df.loc[ix[i], 'regular'].replace(r'/lb','')
if df['sale'].str.contains('/lb').any():
    ix = df[df['sale'].str.contains('/lb')].index
    for i in range(len(ix)):
        df.loc[ix[i], 'sale'] = df.loc[ix[i], 'sale'].replace(r'/lb','')
if df['prime'].str.contains('/lb').any():
    ix = df[df['prime'].str.contains('/lb')].index
    for i in range(len(ix)):
        df.loc[ix[i], 'prime'] = df.loc[ix[i], 'prime'].replace(r'/lb','')

d = df.to_dict('list') # Take our cleaned dataframe and convert it to a dictionary for more cleaning

for i in range(len(d['sale'])):                                                
    if isinstance(d['sale'][i], str) and 'for' in d['sale'][i].split():  
        d['sale'][i] = float(d['sale'][i].split()[2]) / float(d['sale'][i].split()[0])

for i in range(len(d['prime'])):                                                
        if isinstance(d['prime'][i], str) and 'for' in d['prime'][i].split():  
            d['prime'][i] = float(d['prime'][i].split()[2]) / float(d['prime'][i].split()[0])

df = pd.DataFrame.from_dict(d) # turn our dict back into a dataframe



for i in range(len(df[df['sale'].str.contains('¢', na=False)].index)): # Append a '.' to all values that have a cents symbol
    ix = df[df['sale'].str.contains('¢', na=False)].index
    df.loc[ix[i]][3] = '.' + df.loc[ix[i]][3]

for i in range(len(ix)):
    ix = df[df['prime'].str.contains('¢', na=False)].index
    df.loc[ix[i]][4] = '.' + df.loc[ix[i]][4]

try:
    for i in range(len(ix)):
        ix = df[df['regular'].str.contains('¢', na=False)].index
        df.loc[ix[i]][2] = '.' + df.loc[ix[i]][2]
except:
    pass

ix = df[df['prime'].str.contains('¢', na=False)].index
for i in range(len(ix)):
    df.loc[ix[i]][4] = df.loc[ix[i]][4].replace('¢', '')

ix = df[df['regular'].str.contains('¢', na=False)].index
for i in range(len(ix)):
    df.loc[ix[i]][2] = df.loc[ix[i]][2].replace('¢', '')

ix = df[df['sale'].str.contains('¢', na=False)].index
for i in range(len(ix)):
    df.loc[ix[i]][3] = df.loc[ix[i]][3].replace('¢', '')
df = df.sort_index()  
df["regular"] = pd.to_numeric(df["regular"]) # change columns to numeric for visualization
df["sale"] = pd.to_numeric(df["sale"])
df["prime"] = pd.to_numeric(df["prime"])
df['sale_discount'] = 1-df['sale']/df['regular'] # create new feature to show percentage discount of sale price
df['prime_discount'] = 1-df['prime']/df['regular'] # create new feature to show percentage discount of prime price
df['prime_sale_difference'] = df['prime_discount'] - df['sale_discount'] # create new feature to show the difference between sale discount and prime discount
df['discount_bins'] = pd.cut(df.prime_discount, [0,.25,.50,.75, 1], labels=['0% to 25%', '25% to 50%', '50% to 75%', '75% or more'])
df = df.sort_values(by='prime_discount', ascending=False) # sort by difference
from datetime import date
import pickle
path = (r"C:\Users\water\Desktop\WF\WholeFoods-Datascraping-Project-Deployment\Deployment\scraped products dump\WF_Sales_" + str(date.today().strftime("%b_%d_%Y")) + ".pkl")
with open(path, 'wb') as handle:
    pickle.dump(df, handle, protocol=pickle.HIGHEST_PROTOCOL)
    print("Products saved as WF_Sales_" + str(date.today().strftime("%b_%d_%Y")) + ".pkl")
