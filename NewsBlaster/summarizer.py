
import torch
import os
from transformers.pipelines import pipeline
from concurrent.futures import ThreadPoolExecutor
import logging
from tqdm import tqdm


# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    filename='pipeline.log'
)
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6", device=0 if torch.cuda.is_available() else -1)


def summarize_and_save(file_name,input_dir = "raw_articles", output_dir = "summaries"):
    os.makedirs(output_dir, exist_ok=True)
    input_path = os.path.join(input_dir, file_name)
    output_path = os.path.join(output_dir, file_name.replace('.txt', '_summary.txt'))

    try:
        with open(input_path, 'r',encoding = 'utf-8') as file:
            article = file.read()

            if not article.strip():
                logging.warning(f"Empty article found in {input_path}, skipping summarization.")
                return
        article = article[:1024]

        summary = summarizer(article, max_length=90, min_length=30, do_sample=False)[0]['summary_text'] #ignore

        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(summary)#ignore
        logging.info(f"Summary saved to {output_path}")
    except Exception as e:
        logging.error(f"Error processing {input_path}: {e}")

def parallel_summarize(input_dir="raw_articles", output_dir="summaries"):
    os.makedirs(output_dir, exist_ok=True)

    files = [f for f in os.listdir(input_dir) if f.endswith(".txt")][:10]
    print(f"📄 Found {len(files)} files to summarize.")

    with ThreadPoolExecutor(max_workers=6) as executor:
        list(tqdm(
            executor.map(lambda f: summarize_and_save(f, input_dir, output_dir), files),
            total=len(files),
            desc="🧠 Summarizing"
        ))