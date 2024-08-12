import streamlit as st
from streamlit_tags import st_tags, st_tags_sidebar
from datetime import date
import pandas as pd

st.title('College Application Support')

# Keyword/hastags, tweet count and date range(start and end)
keyword = st_tags_sidebar(label='# Enter Keywords:',
                          text='press enter to add more',
                          suggestion=['PhD', 'Fee', 'Waiver'],
                          maxtags=3,
                          key='afrfae')

keyword = st_tags_sidebar(label='# Enter Keywords:',
                          text='press enter to add more',
                          #value=['PhD', 'Fee', 'Waiver'],
                          suggestions=['PhD', 'Masters', 'Bioinformatics', 'Fee', 'Waiver', 'Application'],
                          maxtags=3,
                          key="afrfae")

No_of_tweets = st.sidebar.slider("Number of Tweets: ", 1, 100, 10)
start_date = st.sidebar.date_input("Start Date")
end_date = st.sidebar.date_input("End Date")
Scraped_date = str(date.today())
