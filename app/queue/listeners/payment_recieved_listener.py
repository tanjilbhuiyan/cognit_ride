import pika
import json
from faker import Faker
import psycopg2

from app.queue.handlers.payment_handler import PaymentCommandHandler

fake = Faker()

rabbitmq_url = "amqps://avxpoguo:Da6pggbTCzcN6BiyrTnva-7549c5dU89@fuji.lmq.cloudamqp.com/avxpoguo"
queue_name = "payments_received_queue"


class PaymentReceivedListener:
    def __init__(self):
        self.command_handler = PaymentCommandHandler()

    def callback(self, ch, method, properties, body):
        print("Received message...")
        try:
            if isinstance(body, bytes):
                body = body.decode('utf-8')
            try:
                data = json.loads(body)
                if isinstance(data, str):
                    data = json.loads(data)
            except json.JSONDecodeError:
                data = body
            if not isinstance(data, dict):
                raise ValueError(f"Expected dictionary, got {type(data)}")

            self.command_handler.handle_received_payment(data)
            # Acknowledge the message
            ch.basic_ack(delivery_tag=method.delivery_tag)

        # except psycopg2.errors.UniqueViolation as e:
        #     print(f"Duplicate record detected: {str(e)}")
        #     print(f"This driver (ID: {data['id']}) is already registered")
        #     # Acknowledge the message since it's a known case
        #     ch.basic_ack(delivery_tag=method.delivery_tag)
        # except json.JSONDecodeError as e:
        #     print(f"Error decoding JSON: {str(e)}")
        #     print(f"Invalid message format: {body}")
        #     ch.basic_ack(delivery_tag=method.delivery_tag)
        # except KeyError as e:
        #     print(f"Missing required field: {str(e)}")
        #     print(f"Received data: {data if 'data' in locals() else 'No data parsed'}")
        #     ch.basic_ack(delivery_tag=method.delivery_tag)
        # except ValueError as e:
        #     print(f"Value error: {str(e)}")
        #     print(f"Data type received: {type(data) if 'data' in locals() else 'No data'}")
        #     ch.basic_ack(delivery_tag=method.delivery_tag)
        # except Exception as e:
        #     print(f"Error processing message: {str(e)}")
        #     print(f"Error type: {type(e)}")
        #     print(f"Data that caused error: {data if 'data' in locals() else 'No data parsed'}")
        #     ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            ch.basic_ack(delivery_tag=method.delivery_tag)

    def consume_payment_received_events(self):
        # Establish a connection to RabbitMQ server using pika
        parameters = pika.URLParameters(rabbitmq_url)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        # Declare the queue to ensure it exists
        channel.queue_declare(queue=queue_name, durable=True)
        # exchange_name = 'payment_received_exchange'
        # channel.queue_bind(exchange=exchange_name, queue=queue_name)
        channel.basic_qos(prefetch_count=1)  # Limit the number of messages sent at once
        channel.basic_consume(queue=queue_name, on_message_callback=self.callback)

        print("Waiting for payment received events...")
        # Start consuming messages
        channel.start_consuming()
