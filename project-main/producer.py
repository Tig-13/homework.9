import pika
import json
from faker import Faker
from mongoengine import connect
from models import Contact

# Подключение к MongoDB
connect(host="mongodb+srv://<username>:<password>@cluster0.mongodb.net/<dbname>?retryWrites=true&w=majority")

# Подключение к RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='email_queue')

fake = Faker()

# Генерация контактов
def generate_contacts(n):
    contacts = []
    for _ in range(n):
        contact = Contact(fullname=fake.name(), email=fake.email())
        contact.save()
        contacts.append(str(contact.id))
    return contacts

# Отправка контактов в очередь
def send_to_queue(contact_ids):
    for contact_id in contact_ids:
        message = json.dumps({'contact_id': contact_id})
        channel.basic_publish(exchange='', routing_key='email_queue', body=message)

if __name__ == "__main__":
    contact_ids = generate_contacts(10)  # Генерация 10 контактов
    send_to_queue(contact_ids)
    connection.close()
