import mysql.connector
from mysql.connector import Error

# venv\Scripts\activate


def create_connection():
    """Create and return a database connection."""
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='root',
            database='mess_token_generator'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None

