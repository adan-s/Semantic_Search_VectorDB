from mysql.connector import connect, Error
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# MySQL connection setup
def get_mysql_connection():
    return connect(
        host=DB_HOST,
        port=int(DB_PORT),
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )


def initialize_database():
    try:
        connection = get_mysql_connection()
        cursor = connection.cursor()

        # Create `memory` table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            id INT AUTO_INCREMENT PRIMARY KEY,
            session_id VARCHAR(255) NOT NULL,
            query TEXT NOT NULL,
            response TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        connection.commit()
        cursor.close()
        connection.close()
        print("Database initialized successfully.")
    except Error as e:
        print(f"Error initializing database: {e}")

# Store memory in MySQL
def store_memory(session_id, query, response):
    try:
        connection = get_mysql_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO memory (session_id, query, response)
            VALUES (%s, %s, %s)
            """,
            (session_id, query, response),
        )
        connection.commit()
        cursor.close()
        connection.close()
    except Error as e:
        print(f"Error storing memory: {e}")

# Retrieve memory from MySQL
def retrieve_memory(session_id):
    try:
        connection = get_mysql_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT query, response FROM memory
            WHERE session_id = %s
            ORDER BY created_at ASC
            """,
            (session_id,),
        )
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows
    except Error as e:
        print(f"Error retrieving memory: {e}")
        return []

# Retrieve all available session IDs
def get_all_sessions():
    try:
        connection = get_mysql_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT DISTINCT session_id FROM memory")
        sessions = cursor.fetchall()
        cursor.close()
        connection.close()
        return [session[0] for session in sessions]
    except Error as e:
        print(f"Error retrieving sessions: {e}")
        return []
