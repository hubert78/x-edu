import streamlit as st
from streamlit_tags import st_tags, st_tags_sidebar
from datetime import date
import pandas as pd
from ntscraper import Nitter
import sys
import contextlib

# Function to suppress the sys print output of ntscraper
@contextlib.contextmanager
def suppress_tqdm():
    original_stdout = sys.stdout
    sys.stdout = open('/dev/null', 'w')
    try:
        yield
    finally:
        sys.stdout = original_stdout


# Function to get tweets in a DataFrame
def get_tweets(term, mode, num, since, until):
    tweets = scraper.get_tweets(term, mode=mode, number=num, since=since, until=until)
    
    final_tweets = []
    for tweet in tweets['tweets']:
        tweet_data = [
            tweet['user']['username'], tweet['user']['name'], tweet['user']['avatar'],
            tweet['link'], tweet['text'], tweet['date'], tweet['stats']['likes'],
            tweet['pictures']]
        final_tweets.append(tweet_data)
    
    columns = [
        'username', 'name', 'avatar', 'link', 'text', 'date', 'likes', 'pictures'
    ]
    
    return pd.DataFrame(final_tweets, columns=columns)

# APPLICATION STARTS HERE
st.title('College Application Support')


# Get keywords/hastags, tweet_count and date range(start and end)
keywords = st.text_input('Enter Keywords')
tweet_count = st.slider("# Number of Tweets: ", 1, 20, 10)
start_date = st.date_input("# Start Date")
end_date = st.date_input("# End Date")
scraped_date = str(date.today())
input_submit_button = st.button('Load tweets')

# Check if the scraper is already in session state
if 'scraper' not in st.session_state:
    with suppress_tqdm():
        st.write('App is loading...')
        st.session_state.scraper = Nitter(log_level=1, skip_instance_check=False)

# Retrieve the scraper from session state
scraper = st.session_state.scraper


# When When Input Submission Button is clicked
if input_submit_button:
    tweets = get_tweets(keywords, 'term', tweet_count, str(start_date), str(end_date))
    st.write(tweets)














