from datetime import datetime
import json
import psycopg2
from fastapi import APIRouter, Depends
from app.repository.database import get_db
from app.scalars.payment_recieved_scalars import ReceivedPayment

payment_receiver_router = r = APIRouter()
from app.repository.database import db_user, db_pass, db_name, db_host, db_port

db_params = {
    "dbname": db_name,
    "user": db_user,
    "password": db_pass,
    "host": db_host,
    "port": db_port
}


@r.post("/offline_payment")
def received_payment(data: ReceivedPayment, db=Depends(get_db)):
    # Connect to PostgreSQL
    try:

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
        created_at = datetime.fromtimestamp(int(data['created_at']) / 1000)

        # Prepare data for insertion
        insert_data = (
            data['transaction_id'],
            data['user_id'],
            data['ride_id'],
            json.dumps(data['trip_details']),  # Convert dict to JSONB
            json.dumps(data['fare_breakdown']),  # Convert dict to JSONB
            float(data['amount']),
            data['transaction_status'],
            data['payment_method'],
            json.dumps(data['payment_details']),  # Convert dict to JSONB
            created_at
        )

        # Execute the insert
        cur.execute(insert_query, insert_data)
        conn.commit()

        print(f"Payment data inserted successfully for transaction: {data['transaction_id']}")

        # Close database connection
        cur.close()
        conn.close()
    except Exception as e:
        print(e)

    return "Success"
