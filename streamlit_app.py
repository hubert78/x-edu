import streamlit as st
from streamlit_tags import st_tags, st_tags_sidebar
from datetime import date
import pandas as pd
from ntscraper import Nitter
import openai
import sys
import contextlib

openai.api_key = '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'

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

    if selected_option == 'Other':
        custom_option = st.text_input('Please specify:')

        if custom_option:
            option.append(custom_option)
            return custom_option
        else:
            return 'None'
    else:
        return selected_option
        

# Function for OpenAI feedback on tweet.
def openai_feedback(test, context):
    
    messages = [
        {'role': 'system', 'content': 'You are a helpful assistant making judgment on tweets. Return True if the tweet meets the criteria, and False if it does not meet the criteria.'},
        {'role': 'user', 'content': f'Does this tweet talk explicitly about {context}: {test}. Return True or False'}
    ]

    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages
    )
    return chat.choices[0].message.content


# Function to get tweets in a DataFrame
def get_tweets(term, mode, num, since, until, context):
    tweets = scraper.get_tweets(term, mode=mode, number=num, since=since, until=until)
    
    final_tweets = []
    for tweet in tweets['tweets']:
        if openai_feedback(tweet['text'], context) == 'True':
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

options = ['College admissions', 'Application fee waiver', 'Cold email', 'Other']


# Get keywords/hastags, tweet_count and date range(start and end)
keywords = st.text_input('Enter Keywords')
context = create_dropdown_with_custom_option('Select an option', options)
tweet_count = st.slider("# Number of Tweets: ", 1, 20, 10)
start_date = st.date_input("# Start Date")
end_date = st.date_input("# End Date")
input_submit_button = st.button('Load tweets')


# When When Input Submission Button is clicked
if input_submit_button:
    # Load Nitter
    with suppress_tqdm():
        st.write('Tweets are loading...')
        scraper = Nitter(log_level=1, skip_instance_check=False)

    tweets = get_tweets(keywords, 'term', tweet_count, str(start_date), str(end_date), context)
    display_tweets(tweets)













