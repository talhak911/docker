import os
from sqlmodel import create_engine
connection_string=os.getenv("DATABASE_URL")
engine =create_engine(connection_string)
