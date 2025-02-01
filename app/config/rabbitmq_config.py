import os
from typing import Optional
import pika
from dotenv import load_dotenv

load_dotenv()

class RabbitMQConfig:
    def __init__(self):
        self.host = os.getenv("RABBITMQ_HOST", "localhost")
        self.port = int(os.getenv("RABBITMQ_PORT", "5672"))
        self.username = os.getenv("RABBITMQ_USERNAME", "guest")
        self.password = os.getenv("RABBITMQ_PASSWORD", "guest")
        self.virtual_host = os.getenv("RABBITMQ_VHOST", "/")
        
        # Default exchange settings
        self.exchange_name = "cogni_ride_exchange"
        self.exchange_type = "topic"
        
    def get_connection(self) -> pika.BlockingConnection:
        """Create a new connection to RabbitMQ"""
        credentials = pika.PlainCredentials(self.username, self.password)
        parameters = pika.ConnectionParameters(
            host=self.host,
            port=self.port,
            virtual_host=self.virtual_host,
            credentials=credentials
        )
        return pika.BlockingConnection(parameters)

    def get_channel(self) -> pika.channel.Channel:
        """Get a channel from the connection"""
        connection = self.get_connection()
        channel = connection.channel()
        
        # Declare the exchange
        channel.exchange_declare(
            exchange=self.exchange_name,
            exchange_type=self.exchange_type,
            durable=True
        )
        
        return channel

    def create_queue(self, queue_name: str, routing_key: str) -> Optional[str]:
        """
        Create a queue and bind it to the exchange
        
        Args:
            queue_name: Name of the queue to create
            routing_key: Routing key for the queue
            
        Returns:
            Queue name if successful, None otherwise
        """
        try:
            channel = self.get_channel()
            
            # Declare the queue
            result = channel.queue_declare(queue=queue_name, durable=True)
            queue_name = result.method.queue
            
            # Bind the queue to the exchange
            channel.queue_bind(
                exchange=self.exchange_name,
                queue=queue_name,
                routing_key=routing_key
            )
            
            return queue_name
        except Exception as e:
            print(f"Error creating queue: {str(e)}")
            return None
