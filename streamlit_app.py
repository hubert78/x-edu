import streamlit as st
from streamlit_tags import st_tags, st_tags_sidebar
from datetime import date
import pandas as pd
from ntscraper import Nitter
import openai
import sys
import os
import contextlib
from dotenv import load_dotenv

def configure():
    load_dotenv()

# Function to suppress the sys print output of ntscraper
@contextlib.contextmanager
def suppress_tqdm():
    original_stdout = sys.stdout
    sys.stdout = open('/dev/null', 'w')
    try:
        yield
    finally:
        sys.stdout = original_stdout

# Function to create dropdown menu for criteria selection
def create_dropdown_with_custom_option(label, options):
    selected_option = st.selectbox(label, options)
    if selected_option == 'Other':
        custom_option = st.text_input('Please specify:')
        if custom_option:
            options.append(custom_option)
            return custom_option
        else:
            return 'None'
    else:
        return selected_option

# Function to get tweets in a DataFrame
def get_tweets(term, mode, num, since, until, context):
    tweets = scraper.get_tweets(term, mode=mode, number=num, since=since, until=until)
    
    final_tweets = []
    for tweet in tweets['tweets']:
        tweet_data = [
            tweet['user']['username'], tweet['user']['name'], tweet['user']['avatar'],
            tweet['link'], tweet['text'], tweet['date'], tweet['stats']['likes'],
            tweet['pictures'], False
        ]
        final_tweets.append(tweet_data)
    
    columns = [
        'username', 'name', 'avatar', 'link', 'text', 'date', 'likes', 'pictures', 'Deleted'
    ]
    
    tweets = pd.DataFrame(final_tweets, columns=columns)
    tweets['date'] = pd.to_datetime(tweets['date'], format='%b %d, %Y · %I:%M %p UTC', utc=True)
    tweets['date'] = tweets['date'].dt.strftime('%b %d, %Y')

    tweets.sort_values(by='date', ascending=False, inplace=True)
    return tweets

# Function to build twitter-like rows
def display_tweets(tweets_df):
    for idx, row in tweets_df.iterrows():
        if not row['Deleted']:
            st.write(f"""
            <div style="border: 1px solid #e1e8ed; border-radius: 10px; padding: 15px; margin-bottom: 10px; background-color: #ffffff;">
                <div style="display: flex; align-items: center;">
                    <img src="{row['avatar']}" alt="{row['username']}" style="border-radius: 50%; width: 50px; height: 50px; margin-right: 10px;">
                    <div>
                        <strong>{row['name']}</strong> <span style="color: #657786;">{row['username']}</span>
                        <br>
                        <span style="color: #657786;">{row['date']}</span>
                    </div>
                </div>
                <p style="margin-top: 10px;">{row['text']}</p>
                <div style="margin-top: 10px;">
                    <a href="{row['link']}" target="_blank" style="color: #1da1f2;">View Tweet</a> • 
                    <span style="color: #657786;">{row['likes']} Likes</span>
                </div>
                <div style="margin-top: 10px;">
                    <button onClick="deleteTweet({idx})" style="background-color: #e0245e; color: white; border: none; padding: 5px 10px; border-radius: 5px;">Delete Tweet</button>
                </div>
            </div>
            """, unsafe_allow_html=True)

# Function to delete a tweet
def delete_tweet(tweet_id):
    global tweets_df
    tweets_df.loc[tweet_id, 'Deleted'] = True

# APPLICATION STARTS HERE
st.title('College Application Support')

options = ['College admissions', 'Application fee waiver', 'Cold email', 'Other']

# Get keywords/hastags, tweet_count and date range(start and end)
keywords = st.text_input('Enter Keywords')
context = create_dropdown_with_custom_option('Select an option', options)
tweet_count = st.slider("# Number of Tweets: ", 1, 20, 10)
start_date = st.date_input("# Start Date")
end_date = st.date_input("# End Date")
input_submit_button = st.button('Load tweets')

# Initialize global DataFrame
if 'tweets_df' not in st.session_state:
    st.session_state.tweets_df = pd.DataFrame()

# When Input Submission Button is clicked
if input_submit_button:
    with suppress_tqdm():
        st.write('Tweets are loading...')
        scraper = Nitter(log_level=1, skip_instance_check=False)

    tweets_df = get_tweets(keywords, 'term', tweet_count, str(start_date), str(end_date), context)
    
    if not tweets_df.empty:
        st.session_state.tweets_df = tweets_df
        display_tweets(tweets_df)
    else:
        st.write('Ooops. Something went wrong. Reload tweets.')

# Check for delete button clicks
if st.session_state.tweets_df is not None:
    for idx in st.session_state.tweets_df.index:
        if st.button(f'Delete Tweet {idx}'):
            delete_tweet(idx)
            st.session_state.tweets_df = st.session_state.tweets_df[~st.session_state.tweets_df.index.isin([idx])]
            st.experimental_rerun()
