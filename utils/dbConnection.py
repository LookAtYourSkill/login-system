import json

import mysql.connector
import mysql.connector.cursor

with open("etc/config.json", 'r') as config_file:
    config = json.load(config_file)

host = config['db']['host']
port = config['db']['port']
user = config['db']['user']
password = config['db']['password']
database = config['db']['database']

class Cursor:
    def __init__(self, dictmode=True):
        self.connection = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor(
            dictionary=dictmode)

    def __enter__(self):
        return self.cursor

    def __exit__(self, ext_type, exc_value, traceback):
        self.cursor.close()
        if isinstance(exc_value, Exception):
            self.connection.rollback()
        else:
            self.connection.commit()
        self.connection.close()

    def __iter__(self):
        for i in self.cursor:
            yield

def prepare():
    with Cursor() as cursor:
        cursor.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255) NOT NULL, password VARCHAR(255) NOT NULL, permission INT NOT NULL DEFAULT 0)")
        cursor.execute("CREATE TABLE IF NOT EXISTS sessions (id INT AUTO_INCREMENT PRIMARY KEY, user_id INT NOT NULL, token VARCHAR(255) NOT NULL, FOREIGN KEY (user_id) REFERENCES users(id))")
        cursor.execute("CREATE TABLE IF NOT EXISTS posts (id INT AUTO_INCREMENT PRIMARY KEY, user_id INT NOT NULL, title VARCHAR(255) NOT NULL, content TEXT NOT NULL, FOREIGN KEY (user_id) REFERENCES users(id))")
