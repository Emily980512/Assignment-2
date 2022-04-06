from crypt import methods
import mysql.connector
from flask import Flask, request, Response
import json
import logging
from flask_mysqldb import MySQL
from redis import Redis
from rq import Queue
from crypt import methods
import unicodedata
from flask import Flask, request
import time
from redis import Redis
from rq import Queue, Worker
from rq.job import Job
# from worker import save_to_file
import random
from rq.registry import StartedJobRegistry
from workerNew import send_email

# from flask import Flask, Response, request
# import uuid
# import random

app = Flask(__name__)
table_name = 'tasks_3034504344'

# app.config['MYSQL_HOST'] = 'mysql-container'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'root'
# app.config['MYSQL_DB'] = 'db'
# app.config['port'] = '3306'

# queue = Queue(connection=Redis(host='redis-container'))

r = Redis(host='redis', port=6379)
queue = Queue(connection=r)
mysql = MySQL(app)

def init_db():
    with app.app_context():
        cur = mysql.connection.cursor()
        schema_sql = """
        CREATE TABLE IF NOT EXISTS tasks_3034504344 (
            id integer PRIMARY KEY,
            title varchar(500) NOT NULL,
            is_completed INTEGER NOT NULL DEFAULT 0,
            notify varchar(500) Not NULL
        )
        """
        cur.execute(schema_sql)

def get_db_connection():
    # conn = sqlite3.connect('database.db')
    # conn.row_factory = sqlite3.Row
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'MySQL_Database',
        'port': '3306',
        'database': 'db'
    }
    connection = mysql.connector.connect(**config)
    # cursor = connection.cursor(dictionary=True)

    return connection



@app.route('/', methods=['POST','GET'])
def createTask():
    conn = get_db_connection()
    cursor = conn.cursor()
    if request.method == 'POST':
        task = request.get_json()
        print("This is task: ", task)
        try:
            task_id = random.randint(1,10000000000)
            title, is_completed, notify = task['title'], task['is_completed'], task['notify']
            print(title)
            print(is_completed)
            cursor.execute('INSERT INTO tasks_3034504344 (id, title, is_completed, notify) VALUES (?, ?, ?, ?)',
                     (task_id, title, is_completed, notify))
            
            # lastRowId = cursor.lastrowid
            cursor.close()
            conn.commit()
            conn.close()
            if task['is_completed'] == 1:
                notify = task['notify']
                job = queue.enqueue(send_email, notify)
                job_status = job.id
            return {'id': task_id}, 201
        except:
            return {'error': 'Invalid JSON Body', 'status': 400}, 400
    else:
        tasks = cursor.execute('SELECT * FROM tasks_3034504344').fetchall()
        cursor.close()
        conn.close()
        taskList = list()
        for task in list(tasks):
            taskList.append({
                'id': task['id'],
                'title': task['title'],
                'is_completed': task['is_completed'],
                'notify': task['notify']
            })
        return {'tasks': taskList}, 200 


@app.route('/<string:id>/', methods=['GET', 'PUT', 'DELETE'])
def getById(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    if request.method == 'GET':
        task = cursor.execute('SELECT * FROM tasks_3034504344 WHERE id = ?',
                        (id,)).fetchone()
        conn.close()
        cursor.close()
        if task is None:
                return {'error': 'Invalid ID', 'status': 400}, 400
        # if task['is_completed'] == 1:
        #         notify = task['notify']
        #         job = queue.enqueue(send_email, notify)
        #         job_status = job.id
        return {'task': {
                'id': task['id'],
                'title': task['title'],
                'is_completed': task['is_completed'],
                'notify': task['notify']
                }}, 200

    elif request.method == 'PUT':
        task = request.get_json()
        try:
            title, is_completed, notify = task['title'], task['is_completed'], task['notify']
            cursor.execute('UPDATE tasks_3034504344 SET title = ?, is_completed = ? , notify = ? WHERE id = ?', 
                    (title, is_completed, notify, id))
            conn.commit()
            # task = conn.execute('SELECT * FROM tasks_3036434871 WHERE id = ?', (id,)).fetchone()
            conn.close()
            cursor.close()
            if task['is_completed'] == 1:
                notify = task['notify']
                job = queue.enqueue(send_email, notify)
                job_status = job.id
            return {}
        except:
            return {}
    else:
        cursor.execute('DELETE FROM tasks_3034504344 WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        cursor.close()
        return {}

# init_db()
if __name__ == '__main__':
    app.run(host='0.0.0.0')

