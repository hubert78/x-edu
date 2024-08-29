import streamlit as st
from streamlit_tags import st_tags, st_tags_sidebar
from datetime import date
import pandas as pd
from ntscraper import Nitter
import openai
import sys
import os
import toml
import contextlib
from dotenv import load_dotenv



# Function to suppress the sys print output of ntscraper
@contextlib.contextmanager
def suppress_tqdm():
    original_stdout = sys.stdout
    sys.stdout = open('/dev/null', 'w')
    try:
        yield
    finally:
        sys.stdout = original_stdout

#Function to create dropdown menu for criteria selection
def create_dropdown_with_custom_option(label, options):
    selected_option = st.selectbox(label, options)

    if selected_option in ['Other', 'Type new key']:
        custom_option = st.text_input('Please specify:')

        if custom_option:
            options.append(custom_option)
            return custom_option
        else:
            return 'None'
    else:
        return selected_option

@st.cache_data
def nittered():
    with st.spinner('Fetching tweets...'):
        # Load Nitter
        with suppress_tqdm():
            scraper = Nitter(log_level=1, skip_instance_check=False)
            return scraper


# Function to get tweets in a DataFrame
def get_tweets(term, mode, num, since, until, context):
    tweets = scraper.get_tweets(term, mode=mode, number=num, since=since, until=until)
    
    final_tweets = []
    for tweet in tweets['tweets']:
        #if openai_feedback(tweet['text'], context) == 'True':
        tweet_data = [
            tweet['user']['username'], tweet['user']['name'], tweet['user']['avatar'],
            tweet['link'], tweet['text'], tweet['date'], tweet['stats']['likes'],
            tweet['pictures'], 'None', context, False]
        final_tweets.append(tweet_data)
    
    columns = [
        'username', 'name', 'avatar', 'link', 'text', 'date', 'likes', 'pictures', 'keyword', 'context', 'Deleted'
    ]
    # Creating a DataFrame and Converting the str date to datetime. Then sort it in descending order
    tweets = pd.DataFrame(final_tweets, columns=columns)
    tweets['datetime'] = pd.to_datetime(tweets['date'], format='%b %d, %Y · %I:%M %p UTC', utc=True)

    tweets['date'] = tweets['datetime'].dt.strftime('%b %d, %Y')

    tweets.sort_values(by='datetime', ascending=False, inplace=True)
    return tweets


# Function to build twitter-like rows.
def display_tweets(tweets_df):
    tweet_template = """
    <div style="border: 1px solid #e1e8ed; border-radius: 10px; padding: 15px; margin-bottom: 10px; background-color: #ffffff;">
        <div style="display: flex; align-items: flex-start;">
            <img src="{avatar}" alt="{username}" style="border-radius: 50%; width: 50px; height: 50px; margin-right: 10px;">
            <div>
                <strong>{name}</strong> <span style="color: #657786;">{username}</span> • <span style="color: #657786;">{date}</span>
                <br>
                <p style="margin-top: 10px;">{text}</p>
                <div style="margin-top: 10px;">
                    <a href="{link}" target="_blank" style="color: #1da1f2;">View Tweet</a> • 
                    <span style="color: #657786;">{likes} Likes</span> • 
                    <a href="#" onclick="deleteTweet('{id}'); return false;" style="color: #e0245e;">Delete Tweet</a>
                </div>
            </div>
        </div>
    </div>
    """

    tweets_html = ""
    for idx, row in tweets_df.iterrows():
        if not row['Deleted']:
            tweet_html = tweet_template.format(
                avatar=row['avatar'],
                username=row['username'],
                name=row['name'],
                date=row['date'],
                text=row['text'],
                link=row['link'],
                likes=row['likes'],
                id=idx
            )
            tweets_html += tweet_html

    st.markdown(tweets_html, unsafe_allow_html=True)


# Function to delete a tweet
def delete_tweet(tweet_id, tweets_df):
    tweets_df.loc[tweet_id, 'Deleted'] = True

# Streamlit callback to handle messages from the frontend
def handle_message(message):
    tweet_id = message['data']
    delete_tweet(tweet_id, tweets_df)


def append_to_csv(tweets):
    """
    Appends tweets to a CSV file, ensuring no tweet URL is duplicated.
    
    Parameters:
    - tweets: DataFrame containing tweet data to append.
    """
    file_path = 'tweets.csv'
    
    try:
        # Read existing data from the CSV file
        existing_data = pd.read_csv(file_path)
    except FileNotFoundError:
        # If file does not exist, create an empty DataFrame
        existing_data = pd.DataFrame(columns=tweets.columns)
    
    # Check for duplicate URLs in the existing data
    if 'link' in existing_data.columns:
        existing_links = existing_data['link'].tolist()
    else:
        existing_links = []

    # Filter out duplicate rows based on 'link' column
    new_data = tweets[~tweets['link'].isin(existing_links)]
    
    # Append the new data to the existing data
    updated_data = pd.concat([existing_data, new_data], ignore_index=True)
    
    # Save the updated data back to the CSV file
    updated_data.to_csv(file_path, index=False)

    st.write('Tweets saved successfully!')










# APPLICATION STARTS HERE
st.title("College Application Support")
st.markdown("<style>h1 {text-align: center;}</style>", unsafe_allow_html=True)

options = ['College admissions', 'Application fee waiver', 'Cold email', 'Other']
#configure()


# Get keywords/hastags, tweet_count and date range(start and end)
keywords = st.text_input('Enter Keywords')
context = create_dropdown_with_custom_option('Select tweet context for AI search', options)
tweet_count = st.slider("# Number of Tweets: ", 1, 20, 10)
start_date = st.date_input("Start Date")
end_date = st.date_input("End Date")
dl_twt_col, load_twt_col = st.columns(2)
with dl_twt_col:
    input_submit_button = st.button('Search for tweets')

with load_twt_col:
    load_twt_button = st.button('Load existing tweets')

# State management for save button
if 'save_tweet' not in st.session_state:
    st.session_state.save_tweet = pd.DataFrame()

# State management for 'loaded_tweets'
if 'loaded_tweets' not in st.session_state:
    st.session_state.loaded_tweets = pd.DataFrame()

dl_tweets = pd.DataFrame()
nit = False

# When  Input Submission Button is clicked
if input_submit_button:
    scraper = nittered()
            
    with st.spinner('Checking received data...'):
        # Get tweets from Nitter
        dl_tweets = get_tweets(keywords, 'term', tweet_count, str(start_date), str(end_date), context)
        nit = True

# Check to see if there is a dataframe for the tweets and display them
if dl_tweets is not None and not dl_tweets.empty:
    display_tweets(dl_tweets)

    keyword_selector, save_twt_button = st.columns(2)
    save_keywords = ['Biology', 'Computer Science', 'Essays', 'Other']
    #with keyword_selector: 
    selected_keyword = create_dropdown_with_custom_option('Select or enter a keyword. Example: Biology', save_keywords)
    dl_tweets['keyword'] = dl_tweets['keyword'].replace({'None':selected_keyword})

    if st.button('Save tweets'):
        append_to_csv(dl_tweets)
        #append_to_csv(dl_tweets, 'tweets.csv')  
        st.write('Tweets saved') 
    
elif dl_tweets is None or dl_tweets.empty and nit is True:
    st.write('Failed to get tweets from Twitter. Search again.')



# --- Save tweets to file ---



# When the Load existing tweets button is clicked. 
if load_twt_button:
    try:
        load_tweets = pd.read_csv('tweets.csv')
        #tweets.sort_values(by='date', ascending=False, inplace=True)
        st.session_state.loaded_tweets = load_tweets
    except Exception as e:
        st.write(f'You have no saved tweets')

# Filter and display loaded tweets based on context
if not st.session_state.loaded_tweets.empty:
    st.markdown("---")
    unique_contexts = st.session_state.loaded_tweets['context'].unique()
    
    # Dropdown for filtering by context
    selected_context = st.selectbox('Filter by context:', ['All'] + list(unique_contexts))

    if selected_context != 'All':
        filtered_tweets = st.session_state.loaded_tweets[st.session_state.loaded_tweets['context'] == selected_context]
    else:
        filtered_tweets = st.session_state.loaded_tweets

    filtered_tweets.sort_values(by='datetime', ascending=False, inplace=True)
    display_tweets(filtered_tweets)
    







