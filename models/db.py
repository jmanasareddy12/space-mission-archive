import os
import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host=os.environ["DB_HOST"],
        port=int(os.environ.get("DB_PORT", 4000)),
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_NAME"],
        ssl_ca="isrgrootx1.pem",
        ssl_verify_cert=True,
        ssl_verify_identity=True
    )
