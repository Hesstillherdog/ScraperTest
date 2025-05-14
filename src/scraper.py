import requests
from bs4 import BeautifulSoup


def fetch_quotes(page=1):
    url = f'https://quotes.toscrape.com/page/{page}/'
    resp = requests.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'lxml')
    quotes = []
    for block in soup.select('.quote'):
        text = block.select_one('.text').get_text(strip=True)
        author = block.select_one('.author').get_text(strip=True)
        tags = [t.get_text(strip=True) for t in block.select('.tags .tag')]
        quotes.append({'text': text, 'author': author, 'tags': tags})
    return quotes
