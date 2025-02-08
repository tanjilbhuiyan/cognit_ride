"""
Payment Event Publisher for Cogni-Ride

This module publishes test payment events to RabbitMQ for different payment methods:
1. Card Payment (via Stripe)
2. Cash Payment (collected by driver)
3. Mobile Financial Services (MFS like bKash)

Each payment event includes:
- Trip details (pickup/dropoff locations, distance, duration)
- Fare breakdown (base fare, distance fare, wait time, surge, VAT)
- Payment method specific details
"""

import pika
import json
from datetime import datetime

# RabbitMQ connection credentials
rabbitmq_url = "amqps://avxpoguo:Da6pggbTCzcN6BiyrTnva-7549c5dU89@fuji.lmq.cloudamqp.com/avxpoguo"
queue_name = "payment_transaction_exchange"

# Test payment payloads
# Card payment scenario: Gulshan to Banani trip with 1.2x surge pricing
test_card_payment = {
    "user_id": "507f1f77bcf86cd799439011",
    "ride_id": "RIDE_2024_02_001",
    "trip_details": {
        "pickup_location": {
            "address": "Gulshan 1, Dhaka",
            "latitude": 23.7820,
            "longitude": 90.4163
        },
        "dropoff_location": {
            "address": "Banani 11, Dhaka",
            "latitude": 23.7937,
            "longitude": 90.4066
        },
        "distance_km": 3.5,  # Distance in kilometers
        "duration_minutes": 25,  # Total trip duration
        "wait_time_minutes": 5  # Additional waiting time
    },
    "fare_breakdown": {
        "base_fare": 150.00,  # Starting fare
        "distance_fare": 70.00,  # Rate: 20 tk per km
        "wait_time_fare": 10.50,  # Rate: 2.1 tk per minute
        "surge_multiplier": 1.2,  # 20% surge due to high demand
        "surge_amount": 20.00,
        "vat_percentage": 5,  # Government VAT
        "vat_amount": 12.50,
        "platform_fee": 15.00,  # Fixed platform charge
        "total_fare": 250.50  # Final amount including all charges
    },
    "amount": 250.50,
    "transaction_status": "COMPLETED",
    "created_at": int(datetime.now().timestamp() * 1000),
    "payment_method": "CARD",
    "transaction_id": "TXN_2024_02_001",
    "payment_details": {
        "card_type": "VISA",
        "last_four": "4242",
        "payment_gateway": "stripe"
    }
}

# Cash payment scenario: Uttara to Airport trip with no surge
test_cash_payment = {
    "user_id": "507f1f77bcf86cd799439012",
    "ride_id": "RIDE_2024_02_002",
    "trip_details": {
        "pickup_location": {
            "address": "Uttara Sector 10, Dhaka",
            "latitude": 23.8728,
            "longitude": 90.3979
        },
        "dropoff_location": {
            "address": "Airport Terminal 1, Dhaka",
            "latitude": 23.8513,
            "longitude": 90.4086
        },
        "distance_km": 4.2,
        "duration_minutes": 18,
        "wait_time_minutes": 2
    },
    "fare_breakdown": {
        "base_fare": 120.00,
        "distance_fare": 84.00,  # Rate: 20 tk per km
        "wait_time_fare": 4.00,  # Rate: 2 tk per minute
        "surge_multiplier": 1.0,  # No surge pricing
        "surge_amount": 0.00,
        "vat_percentage": 5,
        "vat_amount": 10.40,
        "platform_fee": 15.00,
        "total_fare": 180.00
    },
    "amount": 180.00,
    "transaction_status": "COMPLETED",
    "created_at": int(datetime.now().timestamp() * 1000),
    "payment_method": "CASH",
    "transaction_id": "TXN_2024_02_002",
    "payment_details": {
        "collected_by": "DRIVER",
        "cash_collected": 200.00,  # Amount given by passenger
        "change_amount": 20.00     # Change returned to passenger
    }
}

# MFS payment scenario: Dhanmondi to Mohammadpur trip with 1.5x surge
test_mfs_payment = {
    "user_id": "507f1f77bcf86cd799439013",
    "ride_id": "RIDE_2024_02_003",
    "trip_details": {
        "pickup_location": {
            "address": "Dhanmondi 27, Dhaka",
            "latitude": 23.7525,
            "longitude": 90.3742
        },
        "dropoff_location": {
            "address": "Mohammadpur Bus Stand, Dhaka",
            "latitude": 23.7662,
            "longitude": 90.3587
        },
        "distance_km": 6.8,
        "duration_minutes": 35,
        "wait_time_minutes": 8
    },
    "fare_breakdown": {
        "base_fare": 150.00,
        "distance_fare": 136.00,  # Rate: 20 tk per km
        "wait_time_fare": 16.00,  # Rate: 2 tk per minute
        "surge_multiplier": 1.5,  # 50% surge due to very high demand
        "surge_amount": 45.00,
        "vat_percentage": 5,
        "vat_amount": 17.35,
        "platform_fee": 15.00,
        "total_fare": 300.00
    },
    "amount": 300.00,
    "transaction_status": "COMPLETED",
    "created_at": int(datetime.now().timestamp() * 1000),
    "payment_method": "MFS",
    "transaction_id": "TXN_2024_02_003",
    "payment_details": {
        "provider": "bKash",
        "provider_transaction_id": "BK7X89Y2Z3",
        "sender_number": "+8801712345678",
        "payment_type": "merchant_pay",
        "gateway_fee": 1.85  # MFS provider charge
    }
}

def publish_payment_event(payment_data):
    """
    Publishes a payment event to RabbitMQ.
    
    Args:
        payment_data (dict): Payment event data including trip details,
                           fare breakdown, and payment information
    
    The function:
    1. Establishes connection to RabbitMQ
    2. Declares a durable exchange and queue
    3. Publishes the payment event with persistence
    4. Handles connection cleanup
    """
    try:
        # Establish connection to RabbitMQ
        parameters = pika.URLParameters(rabbitmq_url)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()

        # Declare exchange and queue with durability for message persistence
        exchange_name = 'payment_transaction_exchange'
        channel.exchange_declare(exchange=exchange_name, exchange_type='direct', durable=True)
        channel.queue_declare(queue=queue_name, durable=True)
        channel.queue_bind(exchange=exchange_name, queue=queue_name)

        # Publish message with persistence enabled
        channel.basic_publish(
            exchange=exchange_name,
            routing_key=queue_name,
            body=json.dumps(payment_data),
            properties=pika.BasicProperties(
                delivery_mode=2,  # Make message persistent
            )
        )

        print(f"Payment event sent: {json.dumps(payment_data, indent=2)}")

    except Exception as e:
        print(f"Error publishing payment event: {str(e)}")
    finally:
        # Ensure connection is closed even if an error occurs
        if connection and not connection.is_closed:
            connection.close()

if __name__ == "__main__":
    # Test all payment scenarios
    print("Publishing card payment event...")
    publish_payment_event(test_card_payment)
    
    print("\nPublishing cash payment event...")
    publish_payment_event(test_cash_payment)
    
    print("\nPublishing MFS payment event...")
    publish_payment_event(test_mfs_payment)
