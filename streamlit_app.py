import streamlit as st
from datetime import date
import pandas as pd

st.title('College Application Support')

# Keyword/hastags, tweet count and date range(start and end)
Hashtag = st.sidebar.text_input("Enter the Hashtag or Keyword of Tweets : ")
No_of_tweets = st.sidebar.slider("Number of Tweets: ", 1, 100, 10)
start_date = st.sidebar.date_input("Start Date (YYYY-MM-DD) : ")
end_date = st.sidebar.date_input("End Date (YYYY-MM-DD) : ")
Scraped_date = str(date.today())
