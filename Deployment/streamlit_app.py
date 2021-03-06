import streamlit as st
import pandas as pd
import pickle
import numpy as np
import pathlib
import subprocess
import os, random, sys, time 
import matplotlib as plt
import plotly.express as px
import plotly.graph_objects as go
from dash_bootstrap_templates import load_figure_template
import platform
import seaborn as sns
from datetime import date
from Spacy_Parser import SpacyParser
#-----------Title/Header----------------------------------------------------------#
st.set_page_config(page_title = "Whole Foods 'On-Sale' Product Insights and Product Recommendation", page_icon = 'https://youssefsultan.github.io/images/LOGOW.png', layout="wide") 
st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)
st.title("Live Whole Foods 'On-Sale' Product Insights") 
st.markdown("""
<nav class="navbar fixed-top navbar-expand-lg navbar-dark" style="background-color: #00674b;">
  <a class="navbar-brand" target="_blank">Youssef Sultan</a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse" id="navbarNav">
    <ul class="navbar-nav">
      <li class="nav-item active">
        <a class="nav-link disabled" href="#">Whole Foods 'On Sale' Insights and Product Recommendation<span class="sr-only">(current)</span></a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="https://github.com/YoussefSultan" target="_blank">GitHub</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="https://youssefsultan.github.io/posts/wholefoods-data-scraper/" target="_blank">Blog Post</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="https://www.linkedin.com/in/youssefsultan/" target="_blank">LinkedIn</a>
      </li>
    </ul>
  </div>
</nav>
""", unsafe_allow_html=True)
#-----------Caption---------------------------------------------------------------#
st.caption("""
This is an app that gives Whole Foods shoppers and Amazon Prime Members the ability to make the most out of their spending and Prime membership when shopping by understanding what is 'on-sale/discounted' at their 
local Whole Foods.  Click 'About this app' to learn more.
""")
#-----------About this app--------------------------------------------------------#
with st.expander('About this app'):
  st.caption("""
This app scrapes unstructured 'on-sale/discounted' product data from each category on the Whole Foods website pertaining to the user's zipcode/store and structures all of the data in a 
DataFrame (similar to an Excel spreadsheet) with added features (columns) such as discounts for normal shoppers, prime members, the difference between the prime discounts and sale discounts
as well as bins (i.e. items in the 40% off to 50% off range). This helps the user understand the types of products on a discount at their local store.

Current app features:
- Query a structured dataset of your Local Whole Foods
- Select other previous users queries
- Visualize dataset(s) insights {Total items on sale, by category, discount range etc.}
- Generate a personalized shopping cart of on-sale items based on word inputs (i.e. 'Avocado, Pasta') with 3 different modes:
    - Optimize shopping cart for the lowest prices
    or
    - Optimize shopping cart for highest discounts
    or
    - Randomize shopping cart simply based on user input
- Search 'on-sale' data of selected dataset based on keyword (i.e. 'Avocado, Pasta')
- Download structured dataset(s) as CSV
- Recommendation system using collaborative filtering
    - Recommends other discounted products in your generated shopping cart based on what other customers purchased together with their items
""")
#----------App startup settings---------------------------------------------------#
if platform.system()=='Windows':                                                  # if system is windows (local env)
  rules = pd.read_csv(str(pathlib.Path(os.getcwd())) + '/rules.csv').drop(columns='Unnamed: 0') # pull association rules from local path
else:                                                                             # if system is streamlit(linux) (local env)
  rules = pd.read_csv(pathlib.Path('Deployment/rules.csv')).drop(columns='Unnamed: 0') 
  @st.cache                                                                       # load streamlit cache
  def chromedriver_download():                                                    # download seleniumbase chromedriver
    os.system('sbase install chromedriver')
    os.system('ln -s /home/appuser/venv/lib/python3.7/site-packages/seleniumbase/drivers/chromedriver')
  chromedriver_download()
#----------Load graph templates---------------------------------------------------#
templates = [
    "bootstrap",
    "minty",
    "pulse",
    "flatly",
    "quartz",
    "cyborg",
    "darkly",
    "vapor",
]
load_figure_template(templates)
cm = sns.light_palette("#FFE5B4", as_cmap=True)
#-------------|Click to receive insights of your Whole Foods|---------------------#
#                                                                                 #
#-------------Pull local path / streamlit path of wholefoods scraper--------------#
cwd = os.getcwd()                                                                 # gets path
scraper_dir = cwd + '\wholefoods_scraper.py' # local deployment path              # gets local path
scraper_dir_deployment = cwd + '/Deployment/wholefoods_scraper.py'                # gets streamlit path
#------------------Input zipcode/scraper subprocess-------------------------------#
if __name__=='__main__':
  with st.expander("Click to receive insights of your Whole Foods"):
      zipcode = st.text_input('Enter your zipcode:', max_chars=5) 
      if zipcode:
          st.write('Getting results, this may take up to two minutes')
          @st.cache(show_spinner=True)
          def scrape():
            if os.path.isfile(scraper_dir): # if local path exists run wholefoods_scraper.py from the local directory
              subprocess.run([f"{sys.executable}", scraper_dir, str(zipcode)])
            if os.path.isfile(scraper_dir_deployment): # if the deployment path run wholefoods_scraper.py from the streamlit path
              subprocess.run([f"{sys.executable}", scraper_dir_deployment, str(zipcode)]) 
          scrape()
      else:
        pass
#----Path for most recent scraped dataset (.pkl) on local path by date time-------# This way we have each scraped .pkl in order to pull from
  path = sorted([f for f in pathlib.Path('scraped products dump').glob("*.pkl")], key=lambda f: f.stat().st_mtime, reverse=True) # sorted path of scraped dataframes
  locpath = sorted([f for f in pathlib.Path('scraped products dump/location').glob("*.pkl")], key=lambda f: f.stat().st_mtime, reverse=True) # sorted path of of scraped dataframes' locations
#----Path for most recent scraped dataset (.pkl) on deployment path by date time--#
  path_deployment = sorted([f for f in pathlib.Path('Deployment/scraped products dump').glob("*.pkl")], key=lambda f: f.stat().st_ctime, reverse=True) # path adjusted for streamlit cloud deployment
  locpath_deployment = sorted([f for f in pathlib.Path('Deployment/scraped products dump/location').glob("*.pkl")], key=lambda f: f.stat().st_ctime, reverse=True) # path adjusted for streamlit cloud deployment
#----Load latest most recent dataframe and its location---------------------------# [The following is done so the app can be worked on in a local environment & streamlit cloud environment]               
try:                                                                              #
  with open(str(path_deployment[0]), 'rb') as handle:                             # Tries to open most recent df using streamlit path
    df = pickle.load(handle)                 
  with open(str(locpath_deployment[0]), 'rb') as handle2:                         # Tries to open location of most recent df
    location = pickle.load(handle2)                
except:                                                                           # If exception error due to not being on streamlit path  
  with open(str(path[0]), 'rb') as handle:                                        # Opens most recent df using local path
    df = pickle.load(handle)                 
  with open(str(locpath[0]), 'rb') as handle2:                                    # Tries to open location of most recent df
    location = pickle.load(handle2)
#---Show last user's query--------------------------------------------------------#                 
with st.expander("Click to show insights of the last user's query in " + str(location) + " or select a previous query."):
  if len(locpath_deployment) == 0:                                                # if streamlit's deployment path is empty that means were on local path 
    selections = []                                 
    for x in locpath:                                                             # iterate through local path of scraped data (.pkl) and append each item path to a list
      selections.append(str(x)[31:])                                              # indexed to hide path from app and only show location                                        
    queryselection = st.selectbox('Select a previous query', tuple(selections))   # create our streamlit selectbox with each selection being a tuple of our 'selections' list
  else:                                                                           # if streamlit's deployment path is not 0, that means were on streamlit path
    selections = []                                                               # repeat lines 131-135
    for x in locpath_deployment:                              
      selections.append(str(x)[42:])
    queryselection = st.selectbox('Select a previous query', tuple(selections))
#---Query selection---------------------------------------------------------------#  
  if queryselection:                                                              # if a query selection from the select box is selected
    if len(locpath_deployment) == 0:                                              # if the streamlit path of datasets' sum is 0 then we're in a local environment                              
      try:                                                                        
        with open(str(pathlib.Path('scraped products dump\\'+queryselection)), 'rb') as handle:             
          df = pickle.load(handle)                                                # load the query selection from local path
        with open(str('scraped products dump\\location\\'+queryselection), 'rb') as handle2:         
          location = pickle.load(handle2)
      except Exception as e:
        st.write(e)
    else:                                                                         # if the streamlit path of datasets' sum is not 0 then were in streamlit's environment
      try:                                                                        # repeat lines 144-150
        with open(str(pathlib.Path('Deployment/scraped products dump/'+queryselection)), 'rb') as handle:             
          df = pickle.load(handle)
        with open(str('Deployment/scraped products dump/location/'+queryselection), 'rb') as handle2:         
          location = pickle.load(handle2)
      except Exception as e:
        st.write(e)
  else:                                                                           # if no query selection has been picked
    try:                                                                          # repeat from lines 119-128
      with open(str(path_deployment[0]), 'rb') as handle:         
        df = pickle.load(handle)
      with open(str(locpath_deployment[0]), 'rb') as handle2:     
        location = pickle.load(handle2)
    except:                                                       
      with open(str(path[0]), 'rb') as handle:                        
        df = pickle.load(handle)
      with open(str(locpath[0]), 'rb') as handle2:                    
        location = pickle.load(handle2)
#---Insights/Visualizations/Graphs------------------------------------------------#  
  
  try:
    st.markdown('There are ' + str(len(df)) + ' items "on-sale" in ' + str(location) + '. ***For a larger view hover over the dataset and click the full screen icon at the top right to filter by feature.***')   

    def fig1():
      orders = list(df.category.value_counts().sort_values(ascending=True).index)
      fig = px.bar(df, title = 'Total items on sale by category',width=2000, category_orders={'category':orders}, hover_data=['product', 'regular', 'sale', 'prime', 'prime_discount'], height=700, y='category', color='prime_discount',template="quartz")
      fig.update_xaxes(title_text='Total number of items on sale')
      fig.update_yaxes(title_text='Categories')
      fig.add_trace(go.Bar(text=df[['category']].value_counts().sort_values(ascending=False)))
      st.plotly_chart(fig, use_container_width=True)

    def fig2():
      orders = list(df.category.value_counts().sort_values(ascending=True).index)
      fig = px.bar(df, title = 'Total items on sale by discount range',width=2000, category_orders={'category':orders}, hover_data=['product', 'regular', 'sale', 'prime', 'prime_discount'], height=700, y='category', color='discount_bins',template="quartz")
      fig.update_xaxes(title_text='Total number of items on sale')
      fig.update_yaxes(title_text='Categories')
      fig.add_trace(go.Bar(text=df[['category']].value_counts().sort_values(ascending=False)))
      st.plotly_chart(fig, use_container_width=True) 

    def fig3():
      fig = px.scatter(df.sort_values(by='category'), x="prime_discount", y="regular", color="category", title="Products: Regular Price vs Prime Discount by Category", hover_data=['product', 'regular', 'sale', 'prime', 'prime_discount'], width=2000, height=900,
      labels={
        "regular": "Regular Prices of Products ($)",
        "prime_discount": "Prime Discount by Percent (%)"
      }, template='darkly')
      st.plotly_chart(fig, use_container_width=True)

    def fig4():
      fig = px.scatter(df.sort_values(by='company'), x="prime_discount", y="regular", color="company", title="Products: Regular Price vs Prime Discount by Company", hover_data=['product', 'regular', 'sale', 'prime', 'prime_discount'], width=2000, height=900,
      labels={
        "regular": "Regular Prices of Products ($)",
        "prime_discount": "Prime Discount by Percent (%)"
      }, template='darkly')
      st.plotly_chart(fig, use_container_width=True)

    def fig5():
      fig = px.scatter(df.sort_values(by='category'), x="prime_discount", y="regular", color="discount_bins", title="Products: Regular Price vs Prime Discount by Discount Range", hover_data=['product', 'regular', 'sale', 'prime', 'prime_discount'], width=2000, height=900,
      labels={
        "regular": "Regular Prices of Products ($)",
        "prime_discount": "Prime Discount by Percent (%)"
      }, template='darkly')
      st.plotly_chart(fig, use_container_width=True)
    st.write(df.style.background_gradient().set_precision(2))
    st.markdown('**Each graph is interactive, view details by hovering over the graph.**') 
    fig1()
    st.markdown('**You can also filter specific items out by clicking on them on the right, double click to filter all items out but the one selected.**')
    fig2()
    fig3()
    fig5()
    fig4()
  except:
    st.write('Debug Mode') 
#---Shopping cart generator-------------------------------------------------------#  
with st.expander("Click here to generate a shopping cart from " + str(location)):
  st.markdown('*if an optimization parameter is not selected, clicking recommend will randomize your cart again as well.')
  price_optimizer = st.checkbox('Optimize for price')
# cart generation by lowest price     
  if price_optimizer:                                                             # price optimizer checkbox
    highest_discount_optimizer = st.checkbox('Optimize for highest discount')     # discount optimizer checkbox
# --------------------------------------------------------------------------------# 1st cart parameter
    if highest_discount_optimizer:
      # if highest discount optimizer is on
      st.markdown('***Note: highest discount items may not always be the lowest priced due to the type of product...***')
      st.markdown('***Note: cart selections will be randomized if no optimization is selected...***')
      input = st.text_input('Enter items as ("Pasta, Chocolate") format')
      try:
        if input:
          input_items = (input.split(', '))
          original_df = df.copy()
          # Optimized Cart Generator with default sorted values (prime_discount Descending)
          shopping_cart = pd.DataFrame(columns=original_df.columns)
          for i in range(len(input_items)):
              try:        
                  try:
                      shopping_cart = pd.concat([shopping_cart,original_df.loc[original_df['product'].str.contains(input_items[i],case=False)].head(1)], join='inner')
                  except Exception as e:
                      print(e)
                      shopping_cart = pd.concat([shopping_cart,original_df.loc[original_df['product'].str.contains(input_items[i].replace(' ','-'),case=False)].head(1)], join='inner')
              except Exception as p:
                  print(p)
          not_prime = st.checkbox('Not a prime member')
          if not_prime:
            st.write("Your total cart as a normal shopper: $" + str(shopping_cart.sale.sum().round(2)))
          else: 
            st.write("Your total cart as a prime member: $" + str(shopping_cart.prime.sum().round(2)))
      except Exception as e:
        st.warning(input + ' is not on sale or the search format is incorrect')
      col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
      with col1:
        st.button('Generate')
      with col2:
        recommend = st.button('Recommend')
      if recommend:
        try:
          SpacyParser = SpacyParser()                                  # instantiate class object with parameter set to false
          original_df['parsed_product'] = SpacyParser.transform(df)
          shopping_cart['parsed_product'] = SpacyParser.transform(shopping_cart)  
          cart_category_list = list(shopping_cart.parsed_product)
          recommendation_cart = pd.DataFrame(columns=original_df.columns)
          try:
            for item in cart_category_list:
                # initiate search of parsed product from first row of generated shopping cart
                # rules[rules.item_A.str.contains(item, case=False)] # dataframe of rules containing the parsed_product of the generated shopping cart
                index = rules[rules.item_A.str.contains(item, case=False)].index # index of rules containing parsed_product of the generated shopping cart
                itemb = list(rules.loc[index, 'item_B'])[int(np.random.randint(9, size=1))] # picks randomly from the top 5 associations of confidence
                recommendation_cart = pd.concat([recommendation_cart,original_df[original_df['parsed_product'] == itemb].sample(1)]) 
          except Exception as e:
            print(e)        
          st.write(shopping_cart.style.background_gradient(cmap=cm).set_precision(2))
          st.markdown('You may also be interested in...')
          st.write(recommendation_cart.style.background_gradient(cmap=cm).set_precision(2))
        except:
          st.warning('generate a shopping cart to create a recommendation')
      else:
        try:
          st.write(shopping_cart.style.background_gradient(cmap=cm).set_precision(2))
        except Exception:
          pass
    else: # ----------------------------------------------------------------------# second cart parameter
      # if highest discount optimizer is off
      input = st.text_input('Enter items as ("Pasta, Chocolate") format')
      try:  
        if input:
          input_items = (input.split(', '))
          original_df = df.copy()
          # Optimized Cart Generator with sort_values 
          shopping_cart = pd.DataFrame(columns=original_df.columns)
          for i in range(len(input_items)):
              try:        
                  try:
                      shopping_cart = pd.concat([shopping_cart,original_df.loc[original_df['product'].str.contains(input_items[i],case=False)].sort_values(['prime', 'prime_discount'], ascending = ('True', 'False')).head(1)], join='inner')
                  except Exception as e:
                      print(e)
                      shopping_cart = pd.concat([shopping_cart,original_df.loc[original_df['product'].str.contains(input_items[i].replace(' ','-'),case=False)].sort_values(['prime', 'prime_discount'], ascending = ('True', 'False')).head(1)], join='inner')
              except Exception as p:
                  print(p)
          not_prime = st.checkbox('Not a prime member')
          if not_prime:
            st.write("Your total cart as a normal shopper: $" + str(shopping_cart.sale.sum().round(2)))
          else: 
            st.write("Your total cart as a prime member: $" + str(shopping_cart.prime.sum().round(2)))
      except Exception as e:
        st.warning(input + ' is not on sale or the search format is incorrect')
      col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
      with col1:
        st.button('Generate')
      with col2:
        recommend = st.button('Recommend')
      if recommend:
        try:
          SpacyParser = SpacyParser()                                  # instantiate class object with parameter set to false
          original_df['parsed_product'] = SpacyParser.transform(df)
          shopping_cart['parsed_product'] = SpacyParser.transform(shopping_cart)  
          cart_category_list = list(shopping_cart.parsed_product)
          recommendation_cart = pd.DataFrame(columns=original_df.columns)
          try:
            for item in cart_category_list:
                # initiate search of parsed product from first row of generated shopping cart
                # rules[rules.item_A.str.contains(item, case=False)] # dataframe of rules containing the parsed_product of the generated shopping cart
                index = rules[rules.item_A.str.contains(item, case=False)].index # index of rules containing parsed_product of the generated shopping cart
                itemb = list(rules.loc[index, 'item_B'])[int(np.random.randint(9, size=1))] # picks randomly from the top 5 associations of confidence
                recommendation_cart = pd.concat([recommendation_cart,original_df[original_df['parsed_product'] == itemb].sample(1)]) 
          except Exception as e:
            print(e)         
          st.write(shopping_cart.style.background_gradient(cmap=cm).set_precision(2))
          st.markdown('You may also be interested in...')
          st.write(recommendation_cart.style.background_gradient(cmap=cm).set_precision(2))
        except:
          st.warning('generate a shopping cart to create a recommendation')
      else:
        try:
          st.write(shopping_cart.style.background_gradient(cmap=cm).set_precision(2))
        except Exception:
          pass
# RANDOMIZED CART  # -------------------------------------------------------------# third cart parameter
  else:
    # use randomized cart feature
    input = st.text_input('Enter items as ("Pasta, Chocolate") format')
    try:  
      if input:
        input_items = (input.split(', '))
        original_df = df.copy()
        # Random Cart Generator
        shopping_cart = pd.DataFrame(columns=original_df.columns) # shopping cart dataframe
        for i in range(len(input_items)):
            try:        
                try:
                    shopping_cart = pd.concat([shopping_cart,original_df.loc[original_df['product'].str.contains(input_items[i],case=False)].sample(1)], join='inner')
                except Exception as e:
                    print(e)
                    shopping_cart = pd.concat([shopping_cart,original_df.loc[original_df['product'].str.contains(input_items[i].replace(' ','-'),case=False)].sample(1)], join='inner')
            except Exception as p:
                print(p)
        not_prime = st.checkbox('Not a prime member')
        if not_prime:
          st.write("Your total cart as a normal shopper: $" + str(shopping_cart.sale.sum().round(2)))
        else: 
          st.write("Your total cart as a prime member: $" + str(shopping_cart.prime.sum().round(2)))
    except Exception as e:
      st.warning(input + ' is not on sale or the search format is incorrect')
    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
    with col1:
      st.button('Generate Randomized')
    with col2:
      recommend = st.button('Recommend')
    if recommend:
      try:    
        SpacyParser = SpacyParser()                                  # instantiate class object with parameter set to false
        original_df['parsed_product'] = SpacyParser.transform(df)
        shopping_cart['parsed_product'] = SpacyParser.transform(shopping_cart)  
        cart_category_list = list(shopping_cart.parsed_product)
        recommendation_cart = pd.DataFrame(columns=original_df.columns)
        try:
          for item in cart_category_list:
              # initiate search of parsed product from first row of generated shopping cart
              # rules[rules.item_A.str.contains(item, case=False)] # dataframe of rules containing the parsed_product of the generated shopping cart
              index = rules[rules.item_A.str.contains(item, case=False)].index # index of rules containing parsed_product of the generated shopping cart
              itemb = list(rules.loc[index, 'item_B'])[int(np.random.randint(9, size=1))] # picks randomly from the top 5 associations of confidence
              recommendation_cart = pd.concat([recommendation_cart,original_df[original_df['parsed_product'] == itemb].sample(1)]) 
        except Exception as e:
          print(e)
          st.warning('generate a shopping cart to create a recommendation')       
        st.write(shopping_cart.style.background_gradient(cmap=cm).set_precision(2))
        st.markdown('You may also be interested in...')
        st.write(recommendation_cart.style.background_gradient(cmap=cm).set_precision(2))
      except:
        st.warning('Generate a shopping cart to make recommendations')
    else:
      try:
        st.write(shopping_cart.style.background_gradient(cmap=cm).set_precision(2))
      except Exception:
        pass
# Dataset search feature----------------------------------------------------------#
with st.expander("Search 'on-sale' data at " + str(location)):
  search_input = st.text_input('Enter items as ("Pasta, Chocolate") format', key=2)
  if search_input:
    original_df = df.copy()
    search_input.split(', ')
    r = search_input.replace(', ','|')
    st.write(original_df.loc[original_df['product'].str.contains(r,case=False)].style.background_gradient(cmap=cm).set_precision(2))
    st.button('Search', key=3)
# Dataset download feature--------------------------------------------------------#
with st.expander("Download 'on-sale' data at " + str(location) + " as a CSV File/Excel Spreadsheet"):
    
  #### Download Parsed Data Frame Button 
  if platform.system()=='Windows':
    excel_download_string = str(pathlib.Path(queryselection)).replace('scraped products dump\location', '')
    excel_download_string = excel_download_string
    excel_download_string = excel_download_string.replace('.pkl', '') + '.csv'
  else:
    excel_download_string = str(pathlib.Path(queryselection)).replace('Deployment/scraped products dump/location', '')
    excel_download_string = excel_download_string
    excel_download_string = excel_download_string.replace('.pkl', '') + '.csv'    

  @st.cache
  def convert_df(df):
    return df.to_csv().encode('utf-8')


  csv = convert_df(df)

  st.download_button(
    "Download as CSV",
    csv,
    excel_download_string,
    "text/csv",
    key='download-csv'
  )
###################################################################################
