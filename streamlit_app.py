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

# Function to build twitter-like rows.
def display_tweets(tweets_df):
    # Define a template for each tweet's HTML
    tweet_template = """
    <div style="border: 1px solid #e1e8ed; border-radius: 10px; padding: 15px; margin-bottom: 10px; background-color: #ffffff;">
        <div style="display: flex; align-items: center;">
            <img src="{avatar}" alt="{username}" style="border-radius: 50%; width: 50px; height: 50px; margin-right: 10px;">
            <div>
                <strong>{username}</strong> <span style="color: #657786;">@{userid}</span>
                <br>
                <span style="color: #657786;">{date}</span>
            </div>
        </div>
        <p style="margin-top: 10px;">{text}</p>
        <div style="margin-top: 10px;">
            <a href="{link}" target="_blank" style="color: #1da1f2;">View Tweet</a> • 
            <span style="color: #657786;">{likes} Likes</span>
        </div>
    </div>
    """

    # Loop through each tweet in the DataFrame and format it using the template
    tweets_html = ""
    for _, row in tweets_df.iterrows():
        tweet_html = tweet_template.format(
            avatar=row['avatar'],
            username=row['username'],
            userid=row['name'],  # Assuming userid and username are the same
            date=row['date'],
            text=row['text'],
            link=row['link'],
            likes=row['likes']
        )
        tweets_html += tweet_html

    # Display the tweets HTML in Streamlit
    st.markdown(tweets_html, unsafe_allow_html=True)


# APPLICATION STARTS HERE
st.title('College Application Support')


# Get keywords/hastags, tweet_count and date range(start and end)
keywords = st.text_input('Enter Keywords')
tweet_count = st.slider("# Number of Tweets: ", 1, 20, 10)
start_date = st.date_input("# Start Date")
end_date = st.date_input("# End Date")
scraped_date = str(date.today())
input_submit_button = st.button('Load tweets')



# When When Input Submission Button is clicked
if input_submit_button:
    # Load Nitter
    with suppress_tqdm():
        st.write('Tweets are loading...')
        scraper = Nitter(log_level=1, skip_instance_check=False)

    tweets = get_tweets(keywords, 'term', tweet_count, str(start_date), str(end_date))
    display_tweets(tweets)














