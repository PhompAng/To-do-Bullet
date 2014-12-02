import MySQLdb
import sqlite3

print "TTTT"

class SQLite(object):
    """ SQLite connection and manipulation tools """
    def __init__(self, db):
        self.connection = sqlite3.connect(db)
        self.cursor = self.connection.cursor()

    def insert_task(self, data):
        sql = "INSERT INTO task (api, title, message, task_type, time) VALUES (:api, :title, :message, :task_type, :time)"
        self.cursor.execute(sql, data)
        self.connection.commit()
