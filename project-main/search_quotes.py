from mongoengine import connect
from models import Quote
import redis

# Подключение к MongoDB
connect(host="mongodb+srv://<username>:<password>@cluster0.mongodb.net/<dbname>?retryWrites=true&w=majority")

# Подключение к Redis
cache = redis.StrictRedis(host='localhost', port=6379, db=0)

def search_by_name(name):
    cached_result = cache.get(f"name:{name}")
    if cached_result:
        return cached_result.decode('utf-8')
    
    quotes = Quote.objects(author__fullname__istartswith=name)
    result = "\n".join([q.quote for q in quotes])
    cache.set(f"name:{name}", result)
    return result

def search_by_tag(tag):
    cached_result = cache.get(f"tag:{tag}")
    if cached_result:
        return cached_result.decode('utf-8')

    quotes = Quote.objects(tags__icontains=tag)
    result = "\n".join([q.quote for q in quotes])
    cache.set(f"tag:{tag}", result)
    return result

if __name__ == "__main__":
    while True:
        user_input = input("Введите команду (например, name:Einstein, tag:life, tags:life,live или exit): ").strip()
        if user_input.startswith("name:"):
            name = user_input.split(":", 1)[1].strip()
            print(search_by_name(name))
        elif user_input.startswith("tag:"):
            tag = user_input.split(":", 1)[1].strip()
            print(search_by_tag(tag))
        elif user_input == "exit":
            break
