import streamlit as st
from streamlit_tags import st_tags, st_tags_sidebar
from datetime import date
import pandas as pd
from ntscraper import Nitter
import sys
import os

st.title('College Application Support')

print('---------------- Hello World-------------------------------------------')
# Keyword/hastags, tweet count and date range(start and end)
keyword = st_tags_sidebar(label='Enter Keywords:',
                          text='press enter to add more',
                          suggestions=['PhD', 'Masters', 'Bioinformatics', 'Fee', 'Waiver', 'Application'],
                          maxtags=3,
                          key="afrfae")

No_of_tweets = st.sidebar.slider("# Number of Tweets: ", 1, 100, 10)
start_date = st.sidebar.date_input("# Start Date")
end_date = st.sidebar.date_input("# End Date")
Scraped_date = str(date.today())
submitted = st.sidebar.button('Find Tweets')

# Redirect stderr to null to avoid tqdm issues
original_stderr = sys.stderr
sys.stderr = open(os.devnull, 'w')

# Initialize the scraper
scraper = Nitter(log_level=None, skip_instance_check=False)

# Restore original stderr
sys.stderr = original_stderr

 




