import pika
from pika.exchange_type import ExchangeType
import json

class MQConsumer:
    def __init__(self):
        self._connection = pika.BlockingConnection(pika.ConnectionParameters('localhost',credentials=pika.PlainCredentials('Worker','workerPassword')))

    def get_messages(self, count):
        current_message = 0
        data = []
        channel = self._connection.channel()
        channel.exchange_declare('SatWorker',exchange_type=ExchangeType.topic,durable=True)
        #print('Collecting messages')
        for method_frame, properties, body in channel.consume('WorkOut',auto_ack=True):
            json_data = json.loads(body)
            data.append(json_data)
            waiting = channel.get_waiting_message_count()
            current_message = current_message + 1
            #print(count, " : ", current_message, " Waiting: ", waiting)
            if(current_message > count):
                if(waiting == 0):
                    channel.close()
        #print('finished collecting messages')
        #channel.close()
        return data

    def disconnect(self):
        self._connection.close()