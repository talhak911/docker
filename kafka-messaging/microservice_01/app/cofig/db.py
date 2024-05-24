from sqlmodel import create_engine
from sqlmodel import SQLModel
from sqlmodel import Session
import os
connection =os.getenv("POSTGRES_URL")
engine = create_engine(connection,connect_args={"sslmode": "require"})

def get_session():
    with Session(engine) as session:
        yield session
        
def create_db_and_tables():
    try:
        SQLModel.metadata.create_all(engine)
    except Exception as e:  # Handle potential errors during table creation
        print(f"Error creating tables: {e}")