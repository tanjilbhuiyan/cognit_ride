import pika
import json

# RabbitMQ connection credentials
rabbitmq_url = "amqps://avxpoguo:Da6pggbTCzcN6BiyrTnva-7549c5dU89@fuji.lmq.cloudamqp.com/avxpoguo"
queue_name = "driver_registration_exchange"


class PublishPaymentSuccess:

    def publish_success_message(self,message: dict):
        try:
            # Establish a connection to RabbitMQ server
            parameters = pika.URLParameters(rabbitmq_url)
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()

            # Declare a queue to send the message to (ensures the queue exists)
            channel.queue_declare(queue=queue_name, durable=True)

            # Send the message
            channel.basic_publish(
                exchange='',
                routing_key=queue_name,
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # Make the message persistent
                )
            )
            print(f"Message sent: {message}")

            # Check the connection status
            if connection.is_open and channel.is_open:
                print("Connection and channel are open. Message sent successfully!")

            # Close the connection gracefully
            connection.close()

        except pika.exceptions.AMQPConnectionError as e:
            print(f"Error: Could not connect to RabbitMQ server. {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
