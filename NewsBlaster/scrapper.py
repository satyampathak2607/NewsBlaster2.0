import requests
from bs4 import BeautifulSoup
import logging
import os

logging.basicConfig(
    filename='pipeline.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

def fetch_article(url, save_dir = "raw_articles"):
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        logging.error(f"Failed to fetch {url} with status code {response.status_code}")
        return 
    
    soup = BeautifulSoup(response.text, 'html.parser')
    paragraphs = soup.find_all('p')
    text = "\n".join(
        p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)
    )

    file_name = url.split("/")[-1][:40].replace("?", "").replace("&", "").replace("=", "") 
    if not file_name.endswith('.txt'):
        file_name += '.txt'
    
    os.makedirs(save_dir, exist_ok=True)
    path = os.path.join(save_dir, file_name)
    with open(path, 'w', encoding='utf-8') as file:
        file.write(text)

    logging.info(f"Saved article from {url} to {path}")

from concurrent.futures import ThreadPoolExecutor

def threaded_fetch(url_list, save_dir = "raw_articles"):
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(lambda url: fetch_article(url, save_dir), url_list)
        

