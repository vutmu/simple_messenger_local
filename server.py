import psycopg2
from flask import Flask, request, abort
import time

app = Flask(__name__)





@app.route("/")
def hello():
    return "Hello, World!<a href='/messenger'>Чатик</a>"


@app.route("/status")
def status():
    messages_count = pgdb('SELECT max(id) FROM messages;')[-1][-1]
    members_count = pgdb('SELECT count(distinct name) FROM messages;')[-1][-1]
    return {'members': members_count,
            'messages_count': messages_count,
            'Status': 'ok'}


@app.route("/messenger")
def messenger():
    if 'after_timestamp' in request.args:
        after_timestamp = float(request.args['after_timestamp'])
    else:
        after_timestamp = 0
    """нужно все строки из БД у которых posting_time больше after_timestamp"""
    query = f" SELECT * FROM messages WHERE posting_time>{after_timestamp} LIMIT 100;"
    dbresponse = pgdb(query)
    return {'messages': dbresponse}

@app.route("/send", methods=['GET', 'POST'])  # получает запрос типа пост из button_pressed месенджера
def send():
    try:
        data = request.json
        query = (data['name'], data['text'], time.time())
        query = f"INSERT INTO messages (name, message, posting_time) VALUES {query}"
        pgdb(query)
        return {'Status': 'ok'}
    except:
        return 'Все норм'


"""нужна функция, которая обращается к базе данных. Она получает запрос или генерирует его из
входящих параметров и возвращает список кортежей."""


def pgdb(query):
    connection = psycopg2.connect(
        database='simple_messenger',
        user='force',
        password='12345',
        host='localhost',
        port='5432',
    )
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute(query)
    try:
        return cursor.fetchall()
    except:
        pass


app.run()
