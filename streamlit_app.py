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
    with suppress_tqdm():  
      tweets = scraper.get_tweets(term, mode=mode, number=num, since=since, until=until)
    
    final_tweets = []
    for tweet in tweets['tweets']:
        tweet_data = [
            tweet['user']['username'], tweet['user']['name'], tweet['user']['avatar'],
            tweet['link'], tweet['text'], tweet['date'], tweet['stats']['likes'],
            tweet['pictures']]
        final_tweets.append(tweet_data)
    
    columns = [
        'username', 'user', 'avatar', 'link', 'text', 'date', 'likes', 'pictures'
    ]
    
    return pd.DataFrame(final_tweets, columns=columns)

# APPLICATION STARTS HERE
st.title('College Application Support')


# Get keywords/hastags, tweet_count and date range(start and end)
keywords = st.text_input('Enter Keywords')
tweet_count = st.slider("# Number of Tweets: ", 1, 100, 10)
start_date = st.date_input("# Start Date")
end_date = st.date_input("# End Date")
scraped_date = str(date.today())
input_submit_button = st.button('Find Tweets')



#with suppress_tqdm():
#    scraper = Nitter(log_level=1, skip_instance_check=False)

st.write(keywords)

# When When Input Submission Button is clicked
if input_submit_button:    
    st.write('App is loading...')
    date_string = start_date.strftime("%Y-%m-%d")
    st.write(date_string)
    #tweets = get_tweets(keywords, 'term', tweet_count, start_date, end_date)
    #st.write(tweets)














