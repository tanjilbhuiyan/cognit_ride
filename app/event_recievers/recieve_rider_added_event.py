import pika
import json
from faker import Faker
import psycopg2
from datetime import datetime
from urllib.parse import quote_plus
from app.repository.database import db_user, db_pass, db_name, db_host, db_port

fake = Faker()

# RabbitMQ connection credentials
rabbitmq_url = "amqps://avxpoguo:Da6pggbTCzcN6BiyrTnva-7549c5dU89@fuji.lmq.cloudamqp.com/avxpoguo"
queue_name = "driver_registration_exchange"

# PostgreSQL connection parameters from database.py
db_params = {
    "dbname": db_name,
    "user": db_user,
    "password": db_pass,
    "host": db_host,
    "port": db_port
}

def callback(ch, method, properties, body):
    print("Received message...")
    try:
        # Decode bytes to string if needed
        if isinstance(body, bytes):
            body = body.decode('utf-8')
        
        # Parse the incoming JSON data - handle potential double encoding
        try:
            # First parse
            data = json.loads(body)
            # Check if it's still a string (double encoded)
            if isinstance(data, str):
                data = json.loads(data)
        except json.JSONDecodeError:
            # If first parse fails, try direct use
            data = body
            
        print(f"Final parsed data type: {type(data)}")
        print(f"Final parsed data content: {data}")

        if not isinstance(data, dict):
            raise ValueError(f"Expected dictionary, got {type(data)}")

        # Connect to PostgreSQL
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()

        # Prepare data for insertion
        insert_data = (
            data['firstName'],
            data['lastName'],
            data['email'],
            data['phone'],
            data['presentAddress'],
            data['status'],
            float(data['rating']),
            datetime.fromtimestamp(int(data['createdAt']) / 1000),  # Convert milliseconds to datetime
            data['licenseType'],
            data['vehicleType']
        )

        # SQL insert statement
        insert_query = """
            INSERT INTO drivers_info 
            (firstname, lastname, email, phone, presentaddress, status, rating, createdat, licensetype, vehicletype)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        # Execute the insert
        cur.execute(insert_query, insert_data)
        conn.commit()
        print("Driver data saved successfully")

        # Close database connection
        cur.close()
        conn.close()

        # Acknowledge the message
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {str(e)}")
        print(f"Invalid message format: {body}")
        ch.basic_nack(delivery_tag=method.delivery_tag)
    except KeyError as e:
        print(f"Missing required field: {str(e)}")
        print(f"Received data: {data if 'data' in locals() else 'No data parsed'}")
        ch.basic_nack(delivery_tag=method.delivery_tag)
    except ValueError as e:
        print(f"Value error: {str(e)}")
        print(f"Data type received: {type(data) if 'data' in locals() else 'No data'}")
        ch.basic_nack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"Error processing message: {str(e)}")
        print(f"Error type: {type(e)}")
        print(f"Data that caused error: {data if 'data' in locals() else 'No data parsed'}")
        ch.basic_nack(delivery_tag=method.delivery_tag)


def consume_rider_events():
    # Establish a connection to RabbitMQ server using pika
    parameters = pika.URLParameters(rabbitmq_url)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # Declare the queue to ensure it exists
    channel.queue_declare(queue=queue_name, durable=True)

    # Set up the consumer to receive messages from the queue
    channel.basic_qos(prefetch_count=1)  # Limit the number of messages sent at once
    channel.basic_consume(queue=queue_name, on_message_callback=callback)

    print("Waiting for driver events...")
    # Start consuming messages
    channel.start_consuming()
