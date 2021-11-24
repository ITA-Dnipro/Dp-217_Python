import json
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
        print("Oops! No kafka on that system.")