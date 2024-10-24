import json
from mongoengine import connect
from models import Author, Quote

# Подключение к MongoDB
connect(host="mongodb+srv://atlasAdmin:@#UfPRHhhY47tsU@cluster0.mongodb.net/<dbname>?retryWrites=true&w=majority")

# Загрузка данных из файла authors.json
def load_authors():
    with open('authors.json', 'r', encoding='utf-8') as f:
        authors_data = json.load(f)
        for author_data in authors_data:
            author = Author(
                fullname=author_data['fullname'],
                born_date=author_data['born_date'],
                born_location=author_data['born_location'],
                description=author_data['description']
            )
            author.save()

# Загрузка данных из файла qoutes.json
def load_quotes():
    with open('qoutes.json', 'r', encoding='utf-8') as f:
        quotes_data = json.load(f)
        for quote_data in quotes_data:
            author = Author.objects(fullname=quote_data['author']).first()
            if author:
                quote = Quote(
                    tags=quote_data['tags'],
                    author=author,
                    quote=quote_data['quote']
                )
                quote.save()

if __name__ == "__
