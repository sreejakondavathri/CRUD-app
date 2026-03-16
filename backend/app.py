from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import time

app = Flask(__name__)
CORS(app)

db = None

# retry connection until MySQL is ready
while db is None:
    try:
        db = mysql.connector.connect(
            host="db",
            user="root",
            password="root",
            database="tasksdb"
        )
        print("Connected to MySQL")
    except:
        print("MySQL not ready, retrying in 5 seconds...")
        time.sleep(5)


@app.route("/tasks", methods=["GET"])
def get_tasks():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tasks")
    result = cursor.fetchall()
    return jsonify(result)


@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.json
    cursor = db.cursor()
    cursor.execute("INSERT INTO tasks (title) VALUES (%s)", (data["title"],))
    db.commit()
    return {"message": "Task added"}


@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM tasks WHERE id=%s", (id,))
    db.commit()
    return {"message": "Deleted"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)