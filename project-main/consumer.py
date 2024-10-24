import pika
import json
from mongoengine import connect
from models import Contact

# Подключение к MongoDB
connect(host="mongodb+srv://<username>:<password>@cluster0.mongodb.net/<dbname>?retryWrites=true&w=majority")

# Функция-заглушка для отправки email
def send_email(contact):
    print(f"Отправка email для {contact.email}...")
    contact.is_sent = True
    contact.save()

# Обработка сообщений из очереди
def callback(ch, method, properties, body):
    data = json.loads(body)
    contact = Contact.objects(id=data['contact_id']).first()
    if contact and not contact.is_sent:
        send_email(contact)

# Подключение к RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='email_queue')

channel.basic_consume(queue='email_queue', on_message_callback=callback, auto_ack=True)

print('Ожидание сообщений. Нажмите CTRL+C для выхода')
channel.start_consuming()
