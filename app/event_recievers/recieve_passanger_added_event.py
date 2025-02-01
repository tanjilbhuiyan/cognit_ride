import pika
import json
from faker import Faker

# Initialize Faker to generate fake data
fake = Faker()

# RabbitMQ connection credentials
rabbitmq_url = "amqps://avxpoguo:Da6pggbTCzcN6BiyrTnva-7549c5dU89@fuji.lmq.cloudamqp.com/avxpoguo"
queue_name = "passenger_registration_exchange"

# MongoDB connection credentials
username = "snewaj"
password = "d5JozZrX66g5sSyD"


# cluster_url = "mongoloadcluster.bdsnb.mongodb.net"
# database_name = "resumeDatabase"  # The name of the database you want to access
# collection_name = "resumes"  # The name of the collection you want to query

# MongoDB URI for connection
# uri = f"mongodb+srv://{username}:{password}@{cluster_url}/?retryWrites=true&w=majority&appName=MongoLoadCluster"


def callback(ch, method, properties, body):
    print("Received message...")
    data = json.loads(body)
    print(f"Message: {data}")
    # Acknowledge the message so it is removed from the queue
    ch.basic_ack(delivery_tag=method.delivery_tag)


def consume_passenger_events():
    # Establish a connection to RabbitMQ server using pika
    parameters = pika.URLParameters(rabbitmq_url)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # Declare the queue to ensure it exists
    channel.queue_declare(queue=queue_name, durable=True)

    # Set up the consumer to receive messages from the queue
    channel.basic_qos(prefetch_count=1)  # Limit the number of messages sent at once
    channel.basic_consume(queue=queue_name, on_message_callback=callback)

    print("Waiting for passangers...")
    # Start consuming messages
    channel.start_consuming()
