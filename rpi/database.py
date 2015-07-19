import sqlite3
import time

class Database(object):
    def __init__(self):
        self.database_file_name = "../rpi.db"
        self.conn = sqlite3.connect(self.database_file_name)
        self.cursor = self.conn.cursor()

    def create_control_table(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS CONTROL (timestamp INTEGER, measured_value INTEGER, pid_value REAL)")
        self.conn.commit()

    def insert_into_control_table(self, measured_value, pid_value):
        self.cursor.execute("INSERT INTO CONTROL VALUES(?, ?, ?)", (time.time(), measured_value, pid_value))
        self.conn.commit()

    def close_connection(self):
        self.conn.close()

# testing purposes
if __name__ == "__main__":
    db = Database()
    db.create_control_table()
    db.insert_into_control_table(123, 123)
    db.close_connection()