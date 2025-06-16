from rss_generator import multi_rss_generator
from scrapper import threaded_fetch
import logging
import os
from summarizer import parallel_summarize

# Set up logging
logging.basicConfig(  
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    filename='pipeline.log'
)

def main():
    logging.info("starting")

    rss_feed_urls = {
    "Firstpost India": "https://www.firstpost.com/commonfeeds/v1/mfp/rss/india.xml",
    "NDTV India": "https://feeds.feedburner.com/ndtvnews-india-news",
    "TOI Top News": "https://timesofindia.indiatimes.com/rssfeeds/-2128936835.cms"
    }
    max_articles = 3

    try:
        logging.info("Starting RSS feed generation")
        urls = list(multi_rss_generator(rss_feed_urls, max_articles))
        logging.info(f"Generated {len(urls)} URLs from RSS feeds")
        logging.info("Starting threaded fetching of articles")
        threaded_fetch(urls)
        logging.info("Threaded fetching completed")

        logging.info("Starting summarization process")
       
       
    except Exception as e:
        logging.error(f"An error occurred: {e}")

    logging.info("Pipeline completed successfully")
    logging.shutdown()

if __name__ == "__main__":
    parallel_summarize(input_dir="raw_articles", output_dir="summaries")
    

    main()
    
    

        




    