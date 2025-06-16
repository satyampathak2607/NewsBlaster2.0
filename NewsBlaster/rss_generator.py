import requests
from bs4 import BeautifulSoup
import logging
# set up logging
logging.basicConfig(
    filename='pipeline.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)


# set up generator function 
def multi_rss_generator(feed_urls, max_articles = 5):

    # set up user agent - headers
    headers = { 'User-Agent': 'Mozilla/5.0'}

    # run the loop for each feed url

    for rss_url in feed_urls:
        try:
            response = requests.get(rss_url, headers=headers)
            if response.status_code!= 200:
                print(f" failed :{rss_url} with status code {response.status_code}")
                continue

            # parse rss xml
            soup = BeautifulSoup(response.content, 'xml') # used xml cuz rss is xml based ##IMPORTANT

            # loop through items
            count = 0 #tracks how many articles we have yielded , last time upar rkha tha
            for item in soup.find_all('item'):

                link_tag = item.find('link') # type: ignore vs code sucks T_T
                if link_tag and link_tag.text:
                    yield link_tag.text.strip() # yield the link of the article

                # limit output
                count += 1
                if count >= max_articles:
                    break
                logging.info(f"Processed {count} articles from {rss_url}")
        except Exception as e:
            logging.error(f"Error processing {rss_url}: {e}")


       
