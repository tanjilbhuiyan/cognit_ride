import pika
import json
from faker import Faker

fake = Faker()

# RabbitMQ connection credentials
rabbitmq_url = "amqps://avxpoguo:Da6pggbTCzcN6BiyrTnva-7549c5dU89@fuji.lmq.cloudamqp.com/avxpoguo"
queue_name = "passenger_registration_exchange"


def callback(ch, method, properties, body):
    print("Received payload...")
    data = json.loads(body)
    print(f"Payload: {data}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def consume_rider_events():
    # Establish a connection to RabbitMQ server using pika
    parameters = pika.URLParameters(rabbitmq_url)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # Declare the queue to ensure it exists
    channel.queue_declare(queue=queue_name, durable=True)
    exchange_name = 'passenger_registration_exchange'  # Name of the exchange created by the other team
    channel.queue_bind(exchange=exchange_name, queue=queue_name)

    # Set up the consumer to receive messages from the queue
    channel.basic_qos(prefetch_count=1)  # Limit the number of messages sent at once
    channel.basic_consume(queue=queue_name, on_message_callback=callback)

    print("Waiting for rider event...")
    # Start consuming messages
    channel.start_consuming()
