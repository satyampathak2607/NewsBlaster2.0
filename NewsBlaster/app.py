import streamlit as st
import os
from rss_generator import multi_rss_generator
from scrapper import threaded_fetch
from summarizer import parallel_summarize
import time



st.set_page_config(page_title="📰 NEWSBLASTER", page_icon="🗿", layout="wide")
st.title("📰 NEWSBLASTER")
if st.button("Refresh"):
    st.cache_data.clear()
    st.rerun()
st.caption("learning basic web scraping, summarization and RSS feed generation with Python along with getting a hang of pipelines and streamlit")

ALL_FEEDS = {
    "Firstpost India": "https://www.firstpost.com/commonfeeds/v1/mfp/rss/india.xml",
    "NDTV India": "https://feeds.feedburner.com/ndtvnews-india-news",
    "TOI Top News": "https://timesofindia.indiatimes.com/rssfeeds/-2128936835.cms"
}

selected_feeds = st.multiselect(
    "Select News Sources",
    options= list(ALL_FEEDS.keys()),
    default = ["Firstpost India"]
)

article_limit = st.slider("Number of Articles per Source", min_value = 1, max_value = 10, value = 3)

if st.button("Run Newsblaster"):
    with st.spinner("Generating RSS feeds..."):
        feed_urls = [ALL_FEEDS[source] for source in selected_feeds]

        urls = list(multi_rss_generator(feed_urls, max_articles = article_limit))

        threaded_fetch(urls)
        parallel_summarize()
    
    st.success("Newsblaster completed successfully!")

    st.subheader("Generated Article URLs:")
    summary_files = os.listdir("summaries")
    for file in summary_files:
        path = os.path.join("summaries", file)
        with open(path, "r", encoding='utf-8') as f:
            summary = f.read()

        with st.expander(file):
            st.write(summary)
