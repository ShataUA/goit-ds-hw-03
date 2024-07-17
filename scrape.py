import requests
from bs4 import BeautifulSoup
import json


def scrape_quotes():
    """Scrape quotes and authors information"""
    base_url = 'http://quotes.toscrape.com'
    all_quotes = []
    all_authors = []

   
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    
    while True:
        quotes = soup.select('div.quote')
        for quote in quotes:
            text = quote.find('span', class_='text').get_text()
            author = quote.find('small', class_='author').get_text()
            tags = [tag.get_text() for tag in quote.select('div.tags a.tag')]
            
            all_quotes.append({
                'quote': text,
                'author': author,
                'tags': tags
            })

            if not any(a['fullname'] == author for a in all_authors):
                author_info = {
                    'fullname': author,
                    'born_date': '',
                    'born_location': '',
                    'description': ''
                }
                
                
                author_page_url = base_url + f'/author/{author.replace(" ", "-")}'
                response_author = requests.get(author_page_url)
                soup_author = BeautifulSoup(response_author.text, 'html.parser')
                
                
                author_birth_date = soup_author.find('span', class_='author-born-date').get_text()
                author_birth_location = soup_author.find('span', class_='author-born-location').get_text()
                author_description = soup_author.find('div', class_='author-description').get_text().strip()
                
               
                author_info['born_date'] = author_birth_date
                author_info['born_location'] = author_birth_location
                author_info['description'] = author_description
                
                all_authors.append(author_info)

        next_button = soup.find('li', class_='next')
        if not next_button:
            break
        
        next_page_url = base_url + next_button.find('a')['href']
        response = requests.get(next_page_url)
        soup = BeautifulSoup(response.text, 'html.parser')
    
    return all_quotes, all_authors


def save_to_json(data, filename):
    """Save json file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    quotes_data, authors_data = scrape_quotes()
    
    save_to_json(quotes_data, 'quotes.json')
    save_to_json(authors_data, 'authors.json')
    
    print('Data saved into quotes.json and authors.json')