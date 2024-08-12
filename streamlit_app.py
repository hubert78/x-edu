import streamlit as st
from streamlit import st_tags
from datetime import date
import pandas as pd

st.title('College Application Support')

# Keyword/hastags, tweet count and date range(start and end)
Hashtag = st.sidebar.st_tags(
  label = 'Add Hashtag or Keywords',
  text = 'press enter to add more',
  suggestion = ['PhD', 'Fee', 'Waiver'],
  maxtags = 3,
  key = 'hash'
)

No_of_tweets = st.sidebar.slider("Number of Tweets: ", 1, 100, 10)
start_date = st.sidebar.date_input("Start Date")
end_date = st.sidebar.date_input("End Date")
Scraped_date = str(date.today())
