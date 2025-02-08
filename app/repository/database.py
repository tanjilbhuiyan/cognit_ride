from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus

# Define the base class for models
Base = declarative_base()

class Database:
    """
    # Initialize the database connection
    >> db = Database("postgresql://user:password@localhost/dbname")
    >> db.connect()

    # Get a session for database operations
    >> session = db.get_session()

    # Perform database operations (example)
    # session.add(...)
    # session.commit()

    # Close the connection when done
    >> db.close()
    """
    def __init__(self, db_url: str):
        self.db_url = db_url
        self.engine = create_engine(db_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def connect(self):
        """Create the database tables if they don't already exist."""
        Base.metadata.create_all(bind=self.engine)
        print("Database tables created successfully!")

    def get_session(self):
        """Return a new session for database operations."""
        return self.SessionLocal()

    def close(self):
        """Close the database connection."""
        if self.engine:
            self.engine.dispose()

# Initialize the database connection
db_user = "erp"
db_pass = "admin@bs617"
db_name = "congiride"
db_host = "10.112.41.193"
db_port = "5432"
SQLALCHEMY_DATABASE_URL = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
db = Database(SQLALCHEMY_DATABASE_URL)

# Dependency to get a new session for each request
def get_db():
    db_session = db.get_session()
    try:
        yield db_session
    finally:
        db_session.close()