import pika
import sys

import pika.spec

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare queue (shared between sender and workers)
channel.queue_declare(queue='task_queue', durable=True)

# Create message from command line arguments
message = ' '.join(sys.argv[1:]) or "Hello Worker!"

# Send message
channel.basic_publish(
    exchange='',
    routing_key='task_queue',
    body=message,
    properties=pika.BasicProperties(
        delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE, 
    )
)

print(f" [x] Sent '{message}'")
connection.close()
