import mysql.connector
from mysql.connector import Error

try:
    connection = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='root',
        database='mess_token_generator'
    )

    if connection.is_connected():
        print("Connection successful!")
        db_info = connection.get_server_info()
        print(f"Connected to MySQL Server version: {db_info}")

except Error as e:
    print(f"Error while connecting to MySQL: {e}")

finally:
    if 'connection' in locals() and connection.is_connected():
        connection.close()
        print("MySQL connection is closed.")
