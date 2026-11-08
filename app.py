
import os
import mysql.connector
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

load_dotenv()

app = Flask(__name__)


# Connect to MySQL database
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT", 3306))
    )


# Home page
@app.route("/")
def home():
    return render_template("index.html")


# GET: Display all tasks
@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM tasks ORDER BY id DESC")
        tasks = cursor.fetchall()
        return jsonify(tasks)

    finally:
        cursor.close()
        connection.close()


# POST: Add a new task
@app.route("/api/tasks", methods=["POST"])
def add_task():
    data = request.get_json(silent=True) or {}
    title = data.get("title", "")

    if not isinstance(title, str) or not title.strip():
        return jsonify({"error": "Task title is required"}), 400

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "INSERT INTO tasks (title) VALUES (%s)",
            (title.strip(),)
        )

        connection.commit()

        return jsonify({
            "message": "Task added successfully",
                "id": cursor.lastrowid,
                "title": title.strip()
        }), 201

    except mysql.connector.Error:
        connection.rollback()
        return jsonify({"error": "Could not add task"}), 500

    finally:
        cursor.close()
        connection.close()


# PUT: Update task completion
@app.route("/api/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json(silent=True) or {}
    completed = data.get("completed")

    if not isinstance(completed, bool):
        return jsonify({"error": "Invalid completed value"}), 400

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "UPDATE tasks SET completed = %s WHERE id = %s",
            (completed, task_id)
        )

        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Task not found"}), 404

        return jsonify({"message": "Task updated successfully"})

    finally:
        cursor.close()
        connection.close()


# DELETE: Delete a task
@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "DELETE FROM tasks WHERE id = %s",
            (task_id,)
        )

        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Task not found"}), 404

        return jsonify({"message": "Task deleted successfully"})

    finally:
        cursor.close()
        connection.close()


# Run application
if __name__ == "__main__":
    app.run(debug=True)
