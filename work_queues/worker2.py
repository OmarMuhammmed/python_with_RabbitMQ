import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)

print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(f" [x] Received {body.decode()}")
    time.sleep(body.count(b'.'))  # simulate long task
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)  # نأكد إن الرسالة اتعالجت


# هنا بنقول: "أنا مش هاخد أكتر من رسالة في نفس الوقت"
channel.basic_qos(prefetch_count=1)

# اشترك في الـ Queue
channel.basic_consume(queue='task_queue', on_message_callback=callback)

# ابدأ في الاستهلاك
channel.start_consuming()
