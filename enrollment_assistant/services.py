import json
import requests
from kafka import KafkaProducer
from django.conf import settings


# Messages will be serialized as JSON
def serializer(message):
    return json.dumps(message).encode('utf-8')


def produce_message(topic, partition):
    # Kafka Producer
    try:
        producer = KafkaProducer(
            bootstrap_servers=settings.KAFKA_SERVER,
            value_serializer=serializer
        )
        producer.send(topic, {
            'user_email': partition['user_email'],
            'subject': partition['subject'],
            'message': partition['message']
        })
    except Exception:
        try:
            url = "http://127.0.0.1:5000/mailing"
            data = {
                'user_email': partition['user_email'],
                'subject': partition['subject'],
                'message': partition['message']}
            data_json = json.dumps(data)
            response = requests.post(url, data=data_json)
            print(response)
        except Exception:
            print("503: Service Unavailable")
