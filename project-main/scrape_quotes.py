import requests
from bs4 import BeautifulSoup
import json

# URL сайту з цитатами
base_url = "http://quotes.toscrape.com"

# Для зберігання цитат та авторів
quotes_data = []
authors_data = []
authors_set = set()  # Для уникнення дублювання авторів

# Функція для отримання даних з однієї сторінки
def scrape_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Отримуємо цитати
    quotes = soup.find_all('div', class_='quote')
    for quote in quotes:
        text = quote.find('span', class_='text').text
        author = quote.find('small', class_='author').text
        tags = [tag.text for tag in quote.find_all('a', class_='tag')]
        
        # Додаємо цитати у список
        quotes_data.append({
            'quote': text,
            'author': author,
            'tags': tags
        })
        
        # Якщо автор ще не був доданий, додаємо його у список авторів
        if author not in authors_set:
            authors_set.add(author)
            author_url = base_url + quote.find('a')['href']
            scrape_author(author_url)
    
    # Переходимо на наступну сторінку, якщо вона існує
    next_page = soup.find('li', class_='next')
    if next_page:
        next_url = base_url + next_page.find('a')['href']
        scrape_page(next_url)

# Функція для збору інформації про авторів
def scrape_author(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    author_name = soup.find('h3', class_='author-title').text.strip()
    birth_date = soup.find('span', class_='author-born-date').text.strip()
    birth_place = soup.find('span', class_='author-born-location').text.strip()
    description = soup.find('div', class_='author-description').text.strip()
    
    authors_data.append({
        'name': author_name,
        'birth_date': birth_date,
        'birth_place': birth_place,
        'description': description
    })

# Старт скрапінгу з першої сторінки
scrape_page(base_url)

# Зберігаємо дані у JSON файли
with open('quotes.json', 'w', encoding='utf-8') as f:
    json.dump(quotes_data, f, ensure_ascii=False, indent=4)

with open('authors.json', 'w', encoding='utf-8') as f:
    json.dump(authors_data, f, ensure_ascii=False, indent=4)

print("Дані успішно збережено у файли quotes.json та authors.json.")
