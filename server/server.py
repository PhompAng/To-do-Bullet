from pushbullet import PushBullet
from time import strftime
import MySQLdb
import config

class Database(object):
    """ A Connection to main database """
    def __init__(self, credential=config.database):
        self.connection = MySQLdb.connect(
            host = credential['host'],
            user = credential['username'],
            passwd = credential['password'],
            db = credential['db']
        )
        self.cursor = self.connection.cursor()

    def get_due_task(self, time):
        """
        Get all dues tasks
        @param time   Time to match with all tasks
        """
        sql = "SELECT * FROM task WHERE time=%s"
        self.cursor.execute(sql, [time])
        return self.cursor.fetchall()

    def delete_task(self, task_id):
        """
        Delete a task from database
        @param id   A task ID
        """
        sql = "DELETE FROM task WHERE id=%s"
        self.cursor.execute(sql, [task_id])
        self.connection.commit()

class Task(object):
    """ A task get from the database """
    def __init__(self, data):
        self.id = data[0]
        self.api = data[1]
        self.title = data[2]
        self.message = data[3]
        self.type = data[4]

    def __str__(self):
        return self.id, self.api, self.title, self.type

    def push(self):
        """ Push a task """
        p = PushBullet(self.api)
        devices = p.getDevices()
        p.pushNote(devices[0]["tdb"], self.title, self.message)

def main():
    database = Database()
    time = strftime("%Y-%m-%d %H:%M:00")
    tasks = database.get_due_task(time)
    print "==== The time is", time, "===="
    for data in tasks:
        task = Task(data)
        task.push()
        database.delete_task(task.id)
    print "Done! See you in a minute (I really mean it!)"
    print "============================================="

main()
