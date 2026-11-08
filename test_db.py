
import os
import mysql.connector
from dotenv import load_dotenv

# Read database credentials
load_dotenv()

try:
    # Connect Python to MySQL
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", 3306)),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

    print("Successfully connected to MySQL!")

    # Create cursor to execute SQL
    cursor = connection.cursor()

    # Retrieve all tasks
    cursor.execute("SELECT * FROM tasks")

    # Fetch database records
    records = cursor.fetchall()

    print("\nTasks in database:")

    for record in records:
        print(record)

    cursor.close()
    connection.close()

    print("\nDatabase connection closed.")

except mysql.connector.Error as error:
    print("MySQL Error:", error)

except Exception as error:
    print("Error:", error)
