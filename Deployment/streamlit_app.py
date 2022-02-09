import streamlit as st
import pandas as pd
import pickle
import pathlib
import subprocess
import os, random, sys, time 
import matplotlib as plt
import plotly.express as px
import plotly.graph_objects as go
from dash_bootstrap_templates import load_figure_template
#----------------------
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
#-----------Title/Header---------------------------------------------------------------#
st.set_page_config(page_title = "WholeFoods 'On-Sale' Product Insights", page_icon = 'https://www.theartof.com/assets/images/book-images/Whole-Foods-Market-Logo-white-background.png', layout="wide") 
st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)
st.title("Live WholeFoods 'On-Sale' Product Insights") 
st.markdown("""
<nav class="navbar fixed-top navbar-expand-lg navbar-dark" style="background-color: #7454DB;">
  <a class="navbar-brand" target="_blank">Youssef Sultan</a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse" id="navbarNav">
    <ul class="navbar-nav">
      <li class="nav-item active">
        <a class="nav-link disabled" href="#">WholeFoods 'On Sale' Insights<span class="sr-only">(current)</span></a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="https://public.tableau.com/views/BodyFatCompositioninMenfromHydrostaticWeighing/DashboardABD?:language=en-US&:display_count=n&:origin=viz_share_link"  target="_blank">Tableau Dashboard Version<span class="sr-only">(current)</span></a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="https://github.com/YoussefSultan" target="_blank">GitHub</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="https://www.linkedin.com/in/youssefsultan/" target="_blank">LinkedIn</a>
      </li>
    </ul>
  </div>
</nav>
""", unsafe_allow_html=True)
###################################################################
cwd = os.getcwd()
scraper_dir = cwd + '\wholefoods_scraper.py'
scraper_dir_deployment = cwd + '/Deployment/wholefoods_scraper.py'
if __name__=='__main__':
  with st.expander("Click to receive insights of your WholeFoods"):
      zipcode = st.number_input('Enter your zipcode:', step=1) 
      if zipcode:
          #@st.cache
          def scrape():
            if os.path.isfile(scraper_dir): # if path exists  
              subprocess.run([f"{sys.executable}", scraper_dir, str(zipcode)]) 
            if os.path.isfile(scraper_dir_deployment): # if path exists
              subprocess.run([f"{sys.executable}", scraper_dir_deployment, str(zipcode)]) 
          scrape()
          st.write('Getting results, make take up to two minutes')
      else:
        pass
####################################################################  
  path = sorted([f for f in pathlib.Path('scraped products dump').glob("*.pkl")], key=lambda f: f.stat().st_mtime, reverse=True)
  locpath = sorted([f for f in pathlib.Path('scraped products dump/location').glob("*.pkl")], key=lambda f: f.stat().st_mtime, reverse=True)

  path_deployment = sorted([f for f in pathlib.Path('Deployment/scraped products dump').glob("*.pkl")], key=lambda f: f.stat().st_ctime, reverse=True)
  locpath_deployment = sorted([f for f in pathlib.Path('Deployment/scraped products dump/location').glob("*.pkl")], key=lambda f: f.stat().st_ctime, reverse=True)


  try:     # Tries to open through streamlit ('Deployment/' string is required for streamlits path)
    with open(str(path_deployment[0]), 'rb') as handle: # loads our saved .pkl back into a variable 
      df = pickle.load(handle)
    with open(str(locpath_deployment[0]), 'rb') as handle2: # loads our saved .pkl back into a variable
      location = pickle.load(handle2)
  except: # if working on local the path is without the 'Deployment/' string
    with open(str(path[0]), 'rb') as handle: # loads our saved .pkl back into a variable
      df = pickle.load(handle)
    with open(str(locpath[0]), 'rb') as handle2: # loads our saved .pkl back into a variable
      location = pickle.load(handle2)
  try:
    st.markdown('There are ' + str(len(df)) + ' items "on-sale" in ' + str(location) + '. ***For a larger view hover over the dataset and click full screen icon at the top right to filter by feature.***')   

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

    st.write(df)
    st.markdown('**Each graph is interactive, view details by hovering over the graph.**') 
    fig1()
    st.markdown('**You can also filter specific items out by clicking on them on the right, double click to filter all items out but the one selected.**')
    fig2()
    fig3()
    fig5()
    fig4()
  except:
    st.write('Debug Mode') 