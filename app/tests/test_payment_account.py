from fastapi.testclient import TestClient
from api import app
from app.repository.database import get_db, Base
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Test database setup
db_user = "erp"
db_pass = quote_plus("admin@bs617")
db_name = "archxpress"
db_host = "localhost"
db_port = "5432"
SQLALCHEMY_DATABASE_URL = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the test database tables
Base.metadata.create_all(bind=engine)


# Override the get_db dependency to use the test database
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_payment_account():
    response = client.post("/api/payment-accounts/", json={"user_id": 1})
    assert response.status_code == 200
    assert response.json()["user_id"] == 1


def test_add_payment_method():
    # First, create a payment account
    client.post("/api/payment-accounts/", json={"user_id": 1})

    # Add a payment method
    response = client.post(
        "/api/payment-accounts/1/payment-methods/",
        json={"name": "Credit Card", "payment_method_type": "credit_card", "details": {"card_number": "1234-5678-9012-3456"}}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Credit Card"


def test_get_payment_methods():
    # Add a payment method first
    client.post(
        "/api/payment-accounts/1/payment-methods/",
        json={"name": "Credit Card", "payment_method_type": "credit_card", "details": {"card_number": "1234-5678-9012-3456"}}
    )

    # Get payment methods
    response = client.get("/api/payment-accounts/1/payment-methods/")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_set_default_payment_method():
    # Add a payment method first
    payment_method = client.post(
        "/api/payment-accounts/1/payment-methods/",
        json={"name": "Credit Card", "payment_method_type": "credit_card", "details": {"card_number": "1234-5678-9012-3456"}}
    ).json()

    # Set as default
    response = client.put(
        f"/api/payment-accounts/1/default-payment-method/",
        json={"payment_method_id": payment_method["id"]}
    )
    assert response.status_code == 200
    assert response.json()["default_payment_method_id"] == payment_method["id"]


def test_get_default_payment_method():
    # Add a payment method and set as default
    payment_method = client.post(
        "/api/payment-accounts/1/payment-methods/",
        json={"name": "Credit Card", "payment_method_type": "credit_card", "details": {"card_number": "1234-5678-9012-3456"}}
    ).json()
    client.put(
        f"/api/payment-accounts/1/default-payment-method/",
        json={"payment_method_id": payment_method["id"]}
    )

    # Get default payment method
    response = client.get("/api/payment-accounts/1/default-payment-method/")
    assert response.status_code == 200
    assert response.json()["id"] == payment_method["id"]