import MySQLdb
import sqlite3

class SQLite(object):
    """ SQLite connection and manipulation tools """
    def __init__(self, db):
        self.connection = sqlite3.connect(db)
        self.cursor = self.connection.cursor()

    def insert_task(self, data):
        sql = "INSERT INTO task (api, title, message, task_type, time) VALUES (:api, :title, :message, :task_type, :time)"
        self.cursor.execute(sql, data)
        self.connection.commit()

class MySQL(object):
    """ MySQL connection and manipulation tools """
    def __init__(self, db_name="psit"):
        self.connection = MySQLdb.connect(host="54.68.172.164",  # your host, usually localhost
                                  user="ubuntu",  # your username
                                  passwd="123456",  # your password
                                  db=db_name)  # name of the data base
        self.cursor = self.connection.cursor()

    def insert_task(self, data):
        sql = "INSERT INTO task (api, title, message, task_type, time) VALUES (%(api)s, %(title)s, %(message)s, %(task_type)s, %(time)s)"
        self.cursor.execute(sql, data)
        self.connection.commit()

    def get_task(self, api):
        sql = "SELECT id, title, message, task_type, time FROM task WHERE api=%s"
        self.cursor.execute(sql, [api])
        return self.cursor.fetchall()
