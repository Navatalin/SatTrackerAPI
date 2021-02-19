import jsons
import pika
from pika.exchange_type import ExchangeType

class MQPublisher(object):
    EXCHANGE = 'SatTrackerWorker'
    QUEUE = 'WorkerIn'
    ROUTING_KEY = 'In'

    def __init__(self, amqp_url) -> None:
        self._connection = None
        self._channel = None

        self._deliveries = None
        self._acked = None
        self._nacked = None
        self._message_number = None

        self._stopping = False
        self._url = amqp_url
        self.is_connected = False
    
    def connect(self):
        print('connecting to mq')
        self._connection = pika.BlockingConnection(pika.ConnectionParameters('localhost',credentials=pika.PlainCredentials('Worker','workerPassword')))
        print('connected, getting channel')
        self._channel = self._connection.channel()
        print('got channel, delcaring exchange')
        self._channel.exchange_declare('SatWorker',exchange_type=ExchangeType.topic,durable=True)

    def publish_message(self, message):
        self._channel.basic_publish(exchange='SatWorker',routing_key='In',body=jsons.dumps(message))

    def disconnect(self):
        self._connection.close()