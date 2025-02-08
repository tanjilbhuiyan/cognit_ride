from datetime import datetime
import json
import psycopg2
from fastapi import APIRouter, Depends, HTTPException
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
        created_at = datetime.fromtimestamp(data.created_at / 1000)

        # Prepare data for insertion using Pydantic model attributes
        insert_data = (
            data.transaction_id,
            data.user_id,
            data.ride_id,
            data.trip_details.json(),  # Convert Pydantic model to JSON string
            data.fare_breakdown.json(),
            float(data.amount),
            data.transaction_status.value,  # Get enum value
            data.payment_method.value,  # Get enum value
            data.payment_details.json(),
            created_at
        )

        # Execute the insert
        cur.execute(insert_query, insert_data)
        conn.commit()

        print(f"Payment data inserted successfully for transaction: {data.transaction_id}")

        # Close database connection
        cur.close()
        conn.close()
        
        return {"status": "success", "transaction_id": data.transaction_id}
        
    except psycopg2.errors.CheckViolation as e:
        print(f"Invalid payment data: {str(e)}")
        if 'conn' in locals() and conn is not None:
            conn.rollback()
            conn.close()
        raise HTTPException(status_code=400, detail="Invalid payment method or transaction status")
    except Exception as e:
        print(f"Error processing payment: {str(e)}")
        if 'conn' in locals() and conn is not None:
            conn.rollback()
            conn.close()
        raise HTTPException(status_code=500, detail=str(e))