import streamlit as st
from streamlit_tags import st_tags, st_tags_sidebar
from datetime import date
import pandas as pd
from ntscraper import Nitter
import sys
#import contextlib


  


# APPLICATION STARTS HERE
st.title('College Application Support')


# Get keywords/hastags, tweet_count and date range(start and end)
keywords = st_tags(label='Enter Keywords:',
                          text='press enter to add more',
                          suggestions=['PhD', 'Masters', 'Bioinformatics', 'Fee', 'Waiver', 'Application'],
                          maxtags=3,
                          key="afrfae")

tweet_count = st.slider("# Number of Tweets: ", 1, 100, 10)
start_date = st.date_input("# Start Date")
end_date = st.date_input("# End Date")
Scraped_date = str(date.today())


input_submit_button = st.sidebar.button('Find Tweets')

#with suppress_tqdm():
#    scraper = Nitter(log_level=1, skip_instance_check=False)

st.subheader('Application Starts Now')
st.write(start_date)

# When When Input Submission Button is clicked
if input_submit_button:
    st.write(start_date)
    #tweets = get_tweets(keywords, 'term', tweet_count, start_date, end_date)
    #st.write(tweets)














