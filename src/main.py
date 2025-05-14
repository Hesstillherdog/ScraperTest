import argparse
from scraper import fetch_quotes
from db_client import MySQLClient


def run_scraper(pages):
    db = MySQLClient()
    db.create_table()
    for page in range(1, pages + 1):
        print(f"Scraping page {page}...")
        quotes = fetch_quotes(page)
        db.insert_quotes(quotes)
        print(f"Inserted {len(quotes)} quotes.")
    db.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='抓取 quotes.toscrape.com 页面数据并存入 MySQL')
    parser.add_argument('-p', '--pages', type=int, default=3, help='爬取页数，默认3页')
    args = parser.parse_args()
    run_scraper(args.pages)
