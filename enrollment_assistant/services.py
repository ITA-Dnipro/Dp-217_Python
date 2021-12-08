import json
from kafka import KafkaProducer, errors
from django.conf import settings


# Messages will be serialized as JSON
def serializer(message):
    return json.dumps(message).encode('utf-8')


def produce_message(topic, partition):
    try:
        # Kafka Producer
        producer = KafkaProducer(
            bootstrap_servers=settings.KAFKA_SERVER,
            value_serializer=serializer
        )
        producer.send(topic, partition)
    except errors.KafkaError as e:
        settings.LOGGER.error(str(e))
