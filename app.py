from flask import Flask, jsonify, request
import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

server = os.getenv('SERVER')
database = os.getenv('DATABASE')
username = os.getenv('DB_USERNAME')
password = os.getenv('PASSWORD')
print(server, database, username, password)
conn = pyodbc.connect(
    f'DRIVER={{ODBC Driver 17 for SQL Server}};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'UID={username};'
    f'PWD={password}'
)

cursor = conn.cursor()

@app.route('/')
def home():
    return 'Hello, This is the Flask app intergrated with azure sql DB!'

@app.route('/students', methods=['GET'])
def get_studets():
    cursor.execute("SELECT * FROM students")
    students = [{'id': row[0], 'name': row[1], 'age': row[2]} for row in cursor.fetchall()]
    return jsonify(students)

@app.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()
    cursor.execute("INSERT INTO students (name, age) VALUES (?, ?);", data['name'], data['age'])
    conn.commit()
    return jsonify({"message":"student successfully added"}), 201


@app.route('/students/<int:id>', methods=['PUT'])
def update_student(id):
    data = request.get_json()
    cursor.execute("UPDATE students SET name=?, age=? WHERE id=?", data['name'], data['age'], id)
    conn.commit()
    return jsonify({"message":f"student with id {id} successfully updated"}), 200

@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    cursor.execute("DELETE FROM students WHERE id=?", id)
    conn.commit()
    return jsonify({"message":f"student with id {id} successfully deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)
