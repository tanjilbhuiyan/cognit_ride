import pika
import json
import psycopg2
from datetime import datetime
from app.repository.database import db_user, db_pass, db_name, db_host, db_port
from app.models.payment import Payment

# RabbitMQ connection credentials
rabbitmq_url = "amqps://avxpoguo:Da6pggbTCzcN6BiyrTnva-7549c5dU89@fuji.lmq.cloudamqp.com/avxpoguo"
queue_name = "payment_transaction_exchange"

# PostgreSQL connection parameters
db_params = {
    "dbname": db_name,
    "user": db_user,
    "password": db_pass,
    "host": db_host,
    "port": db_port
}

def callback(ch, method, properties, body):
    print("Received payment event...")
    
    try:
        # Decode bytes to string if needed
        if isinstance(body, bytes):
            body = body.decode('utf-8')

        # Parse the incoming JSON data
        try:
            json_data = json.loads(body)
            if isinstance(json_data, str):
                json_data = json.loads(json_data)  # Handle double-encoded JSON
        except json.JSONDecodeError:
            json_data = body
            
        # Convert to Pydantic model
        payment = Payment(**json_data)
        print(f"Payment data validated: {payment.json()}")

        # Connect to PostgreSQL
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()

        # SQL insert statement for ride_payments table
        insert_query = """
            INSERT INTO ride_payments (
                transaction_id,
                user_id,
                ride_id,
                trip_details,
                fare_breakdown,
                amount,
                transaction_status,
                payment_method,
                payment_details,
                created_at
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
        """

        # Convert timestamp from milliseconds to datetime
        created_at = datetime.fromtimestamp(payment.created_at / 1000)

        # Prepare data for insertion using Pydantic model
        insert_data = (
            payment.transaction_id,
            payment.user_id,
            payment.ride_id,
            payment.trip_details.json(),  # Convert Pydantic model to JSON string
            payment.fare_breakdown.json(),
            payment.amount,
            payment.transaction_status.value,  # Get enum value
            payment.payment_method.value,  # Get enum value
            payment.payment_details.json(),
            created_at
        )

        # Execute the insert
        cur.execute(insert_query, insert_data)
        conn.commit()

        print(f"Payment data inserted successfully for transaction: {payment.transaction_id}")

        # Close database connection
        cur.close()
        conn.close()

        # Acknowledge the message
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except psycopg2.errors.UniqueViolation as e:
        print(f"Duplicate payment record: {str(e)}")
        print(f"Transaction ID or Ride ID already exists")
        # Acknowledge the message since it's a known case
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {str(e)}")
        print(f"Invalid message format: {body}")
        ch.basic_nack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"Error processing payment: {str(e)}")
        ch.basic_nack(delivery_tag=method.delivery_tag)
        if 'conn' in locals() and conn is not None:
            conn.rollback()
    finally:
        if 'conn' in locals() and conn is not None:
            conn.close()

def consume_payment_events():
    """
    Consumes payment events from RabbitMQ and stores them in the database.
    """
    # Establish connection
    parameters = pika.URLParameters(rabbitmq_url)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # Declare the queue to ensure it exists
    channel.queue_declare(queue=queue_name, durable=True)
    
    # Bind to the exchange
    exchange_name = 'payment_transaction_exchange'
    channel.queue_bind(exchange=exchange_name, queue=queue_name)

    # Set up the consumer
    channel.basic_qos(prefetch_count=1)  # Process one message at a time
    channel.basic_consume(queue=queue_name, on_message_callback=callback)

    print("Waiting for payment events...")
    channel.start_consuming()

if __name__ == "__main__":
    consume_payment_events()
