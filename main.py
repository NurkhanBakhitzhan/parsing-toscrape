import requests
from bs4 import BeautifulSoup
import json
import csv

def fetch_quotes(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    quotes = []

    for quote in soup.find_all('div', class_='quote'):
        text = quote.find('span', class_='text').get_text()
        author = quote.find('small', class_='author').get_text()
        tags = [tag.get_text() for tag in quote.find_all('a', class_='tag')]
        quotes.append({
            'text': text,
            'author': author,
            'tags': tags
        })
    return quotes

def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def save_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Text', 'Author', 'Tags'])
        for quote in data:
            writer.writerow([quote['text'], quote['author'], ', '.join(quote['tags'])])

if __name__ == "__main__":
    url = 'http://quotes.toscrape.com/'
    quotes = fetch_quotes(url)
    
    save_to_json(quotes, 'quotes.json')
    save_to_csv(quotes, 'quotes.csv')

    print('Data saved to quotes.json and quotes.csv')
