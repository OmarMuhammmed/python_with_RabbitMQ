import pika

"""
Create new instance for Connection Objcet.
If we wanted to connect to a broker on a different machine we'd simply specify
its name or IP address here 'localhost' (if You use Docker or Cloud Service)
"""

# Create a Connection Object
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
# Create a Channel
channel = connection.channel()


""" Declare a queue named 'hello' on the RabbitMQ server """
# Create a Queue
channel.queue_declare(queue='hello')

channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
print(" [x] Sent 'Hello World!'")

connection.close()
