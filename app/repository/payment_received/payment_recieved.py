from app.garbage.models.payment import Payment
from datetime import datetime
from app.repository.database import db_user, db_pass, db_name, db_host, db_port
import psycopg2


class PaymentReceivedRepository:
    def __init__(self):
        """
        Initializes the repository with a database connection.

        :param db_connection: A database connection object (e.g., from psycopg2, SQLAlchemy, etc.).
        """
        self.db_params = {
            "dbname": db_name,
            "user": db_user,
            "password": db_pass,
            "host": db_host,
            "port": db_port
        }

    def save_payment(self, aggregate_root):
        """
        Saves the aggregate root to the database.

        :param aggregate_root: An instance of an aggregate root (e.g., PaymentAggregateRoot).
        """
        conn = psycopg2.connect(**self.db_params)
        cur = conn.cursor()

        try:
            # Convert the aggregate root to a dictionary or other format suitable for DB storage
            payment = Payment(**aggregate_root.data)

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


        except Exception as e:
            print(f"Error saving payment to the database: {str(e)}")
            raise  # Re-raise the exception for further handling if needed
