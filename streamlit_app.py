import streamlit as st
from streamlit_tags import st_tags, st_tags_sidebar
from datetime import date
import pandas as pd
from Scweet.scweet import scrape

st.title('College Application Support')
#scraper = Nitter()

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
 

data = scrape(words=['PhD Bioinformatics'], since="2024-10-01", until="2024-10-05", from_account = None, 
              interval=1, headless=False, display_type="Top", save_images=False, lang="en", 
              resume=False, filter_replies=False, proximity=False)
data


