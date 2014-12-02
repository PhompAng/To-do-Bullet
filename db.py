import MySQLdb
import sqlite3
import default_conf

class SQLite(object):
    """ SQLite connection and manipulation tools """
    def __init__(self, db="db.db"):
        """ 
        @param db  A database filename (use db.db) as a default
        """
        self.connection = sqlite3.connect(db)
        self.cursor = self.connection.cursor()

    def insert_task(self, data):
        """
        Save a task to database 
        @param data   A dict of task data (api, title, message, task_type, time)
        """
        sql = "INSERT INTO task (api, title, message, task_type, time, remote_id) VALUES (:api, :title, :message, :task_type, :time, :remote_id)"
        self.cursor.execute(sql, data)
        self.connection.commit()

    def get_task(self, api):
        """
        Retrieve all task from database where given API_key is matched
        @param api   A user's API key
        """
        sql = "SELECT id, title, message, task_type, time FROM task WHERE api=:api"
        self.cursor.execute(sql, {'api': api})
        return self.cursor.fetchall()

    def delete_task(self, id):
        """
        Delete a task from database
        @param id   A task ID
        """
        sql = "DELETE FROM task WHERE id=:id"
        self.cursor.execute(sql, {'id': id})
        self.connection.commit()

    def get_remote_id(self, local_id):
        """
        Get a remote ID of a task
        @param local_id   A local task id
        """
        sql = "SELECT remote_id FROM task WHERE id=:id"
        self.cursor.execute(sql, {'id': local_id})
        return self.cursor.fetchone()[0]

class MySQL(object):
    """ MySQL connection and manipulation tools """
    def __init__(self, config=default_conf.config):
        """ 
        @param config   A dict of MySQL Connection (contain 'host', 'user', 'passwd', 'db' as a key)
                        User default if this is not given by user
        """
        self.connection = MySQLdb.connect(host=config['host'],  # your host, usually localhost
                                  user=config['user'],  # your username
                                  passwd=config['passwd'],  # your password
                                  db=config['db'])  # name of the data base
        self.cursor = self.connection.cursor()

    def insert_task(self, data):
        """
        Save a task to database 
        @param data   A dict of task data (api, title, message, task_type, time)
        """
        sql = "INSERT INTO task (api, title, message, task_type, time) VALUES (%(api)s, %(title)s, %(message)s, %(task_type)s, %(time)s)"
        self.cursor.execute(sql, data)
        self.connection.commit()
        return self.cursor.lastrowid

    def get_task(self, api):
        """
        Retrieve all task from database where given API_key is matched
        @param api   A user's API key
        """
        sql = "SELECT id, title, message, task_type, time FROM task WHERE api=%s"
        self.cursor.execute(sql, [api])
        return self.cursor.fetchall()

    def delete_task(self, remote_id):
        """
        Delete a task from database
        @param id   A task ID
        """
        sql = "DELETE FROM task WHERE id=%s"
        self.cursor.execute(sql, [remote_id])
        self.connection.commit()
