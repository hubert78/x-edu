import streamlit as st

st.title('*College Application Support*')

# Keyword/hastags, tweet count and date range(start and end)
Hashtag = st.sidebar.text_input("Enter the Hashtag or Keyword of Tweets : ")
No_of_tweets = st.sidebar.number_input("Number of Tweets needed : ", min_value= 1, max_value= 1000, step= 1)
st.sidebar.write(":green[Select the Date range]")
start_date = st.sidebar.date_input("Start Date (YYYY-MM-DD) : ")
end_date = st.sidebar.date_input("End Date (YYYY-MM-DD) : ")
Scraped_date = str(date.today())
