import streamlit as st
import pandas as pd
import pickle
import os, random, sys, time 
import matplotlib as plt
import plotly.express as px
import plotly.graph_objects as go
from data_scrape import wholefoods_scrape
from data_clean import wholefoods_clean
#----------------------
#-----------Title/Header---------------------------------------------------------------#
st.set_page_config(page_title = "Whole Foods Sale Products Insights", page_icon = 'https://store-images.s-microsoft.com/image/apps.59154.13510798882997587.2b08aa2f-aa3f-4d80-a325-a658dbc1145a.2829662d-e5e1-4fdd-bd00-29895e686f94', layout="wide") 
st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)
st.title("Whole Foods Sale Products Insights")
#st.write("""### We need some information to predict your Body Fat Percentage""") 
st.markdown("""
<nav class="navbar fixed-top navbar-expand-lg navbar-dark" style="background-color: #7454DB;">
  <a class="navbar-brand" target="_blank">Youssef Sultan</a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse" id="navbarNav">
    <ul class="navbar-nav">
      <li class="nav-item active">
        <a class="nav-link disabled" href="#">WholeFoods Web<span class="sr-only">(current)</span></a>
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

store = wholefoods_clean()
store.cleaner()
df = store.df 

st.write(df.head(500)) 