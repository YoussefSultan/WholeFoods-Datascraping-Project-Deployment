# Live Whole Foods 'On-Sale' Product Insights and Recommendation System Web Application

![](https://raw.githubusercontent.com/YoussefSultan/WholeFoods-Datascraping-Project-Deployment/main/visuals/wf_app_visual.png)

## The point of this app is to help Whole Foods shoppers know what is on-sale at their local store to save money, with *specifics* that are not given by Whole Foods themselves.

### What this app does: 

- It shows many graphs of live data of all 'on-sale/discounted' items from the user's store to understand how much of each product/category is on sale (see more on this here)

- It generates a shopping cart of items 'on-sale/discounted' based on user keyword input and selected paramter. 

- It recommends products to the user based on Instacart customer data using a collaborative filtering approach and the users generated shopping cart

### How this app's data is collected:
- Scrapes unstructured product data from each category on the Whole Foods website pertaining to the user's zipcode/store and then structures all of the data in a DataFrame (similar to an Excel spreadsheet)


- Any user queried data gets wrangled/cleaned/manipulated in a way to fit all website element changes and gets structured in a perfect readable format with the following columns:
```
company                   object [product company name]
product                   object [product title]
regular                  float64 [regular product price]
sale                     float64 [on-sale product price] 
prime                    float64 [on-sale product price for prime members]
category                  object [Whole Foods category]
sale_discount            float64 [sale discount percentage]
prime_discount           float64 [prime discount percentage]
prime_sale_difference    float64 [prime discount - sale discount]
discount_bins             object [discount bins I.E. 0% Off to 10% off]
```

![](https://raw.githubusercontent.com/YoussefSultan/WholeFoods-Datascraping-Project-Deployment/main/visuals/wf_cf_visual.png)


Current app features:

Query a structured dataset of your Local Whole Foods
Select other previous users queries
Visualize dataset(s) insights {Total items on sale, by category, discount range etc.}
Generate a personalized shopping cart of on-sale items based on word inputs (i.e. 'Avocado, Pasta') with 3 different modes:
Optimize shopping cart for the lowest prices or
Optimize shopping cart for highest discounts or
Randomize shopping cart simply based on user input
Search 'on-sale' data of selected dataset based on keyword (i.e. 'Avocado, Pasta')
Download structured dataset(s) as CSV
Recommendation system using collaborative filtering
Recommends other discounted products in your generated shopping cart based on what other customers purchased together with their items

This [project](https://share.streamlit.io/youssefsultan/wholefoods-datascraping-project-deployment/main/Deployment/streamlit_app.py) is in the works and will be finished soon.

## Tutorial on how to use the app
This app generates shopping carts of items 'on-sale/discounted' by scraping unstructured product data from each category on the Whole Foods website pertaining to the user's zipcode/store and then structures all of the data in a DataFrame (similar to an Excel spreadsheet). 
![](https://raw.githubusercontent.com/YoussefSultan/WholeFoods-Datascraping-Project-Deployment/main/visuals/scrape_animation.gif)
![](https://raw.githubusercontent.com/YoussefSultan/WholeFoods-Datascraping-Project-Deployment/main/visuals/wf_app_visual.gif)
![](https://raw.githubusercontent.com/YoussefSultan/WholeFoods-Datascraping-Project-Deployment/main/visuals/query_animation.gif)
![](https://raw.githubusercontent.com/YoussefSultan/WholeFoods-Datascraping-Project-Deployment/main/visuals/generate_cart.gif)
![](https://raw.githubusercontent.com/YoussefSultan/WholeFoods-Datascraping-Project-Deployment/main/visuals/recommend.gif)
