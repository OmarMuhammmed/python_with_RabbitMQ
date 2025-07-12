import pika


def on_message_recived(ch, method, properties, body):
    print(f"Received: '{body.decode()}'")
    ch.basic_ack(delivery_tag=method.delivery_tag)


conn_parms = pika.ConnectionParameters('localhost')
conn = pika.BlockingConnection(conn_parms)

channel = conn.channel()

channel.queue_declare(queue='testqueue',
                      arguments={
                          'x-max-length': 100000,
                          'x-queue-type': 'classic',
                      },
                      durable=True,
                      )

channel.basic_qos(prefetch_count=1)

channel.basic_consume(
    queue='testqueue',
    on_message_callback=on_message_recived
)

print(" [*] Waiting for messages. To exit press CTRL+C")
channel.start_consuming()
