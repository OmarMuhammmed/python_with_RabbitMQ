from __future__ import absolute_import, unicode_literals
import os
import kombu
from celery import Celery, bootsteps

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookstore.settings')

app = Celery('bookstore')


app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


# setting Rabbit-MQ Publisher
with app.pool.acquire(block=True) as conn:
    exchange = kombu.Exchange(
        name='test_exchange',
        type='direct',
        channel=conn,
        durable=True
    )
    exchange.declare()

    queue = kombu.Queue(
        name='testqueue',
        exchange=exchange,
        routing_key='test-key',
        channel=conn,
        message_timeout=600,
        queue_arguments={
            'x-max-length': 100000,
            'x-queue-type': 'classic',
        },
        durable=True
    )
    queue.declare()


# Consumer 
class TestConsumer(bootsteps.ConsumerStep):
    
    def get_consumers(self, channel):
        return [kombu.Consumer(
            channel,
            queues=[queue],
            callbacks=[self.handle_message],
            accept=['json']
        )]
    
    def handle_message(self, body, message):
        print("Recived Message : {0!r}".format(body))
        message.ack()


