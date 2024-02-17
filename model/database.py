import os
from google.cloud.sql.connector import Connector
from google.cloud import storage
import sqlalchemy
import pymysql

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./bsid-user-group4-sa-key.json"
storage_client = storage.Client()

# initialize Connector object
connector = Connector()

# function to return the database connection
def getconn() -> pymysql.connections.Connection:
    conn: pymysql.connections.Connection = connector.connect(
        "tsmchack2023-bsid-grp4:asia-east1:tsmchack2023-bsid-mysql-db",
        "pymysql",
        user="root",
        password="PfTfq8Mn",
        db="Parking"
    )
    return conn

# create connection pool
pool = sqlalchemy.create_engine(
    "mysql+pymysql://",
    creator=getconn,
)