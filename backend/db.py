import mysql.connector
from mysql.connector import Error
import hashlib

class Database:
    def __init__(self):
        self._connection = None

    def connect(self, host='localhost', user='root', password='', database='proctorai'):
        try:
            self._connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            if self._connection.is_connected():
                print(f"Successfully connected to MySQL database '{database}' on '{host}'")
            return self._connection.is_connected()
        except Error:
            self._connection = None
            return False

    def is_connected(self):
        return self._connection is not None and self._connection.is_connected()

    def get_proctors(self):
        if not self.is_connected():
            return []
        with self._connection.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM users WHERE user_role = 'proctor'")
            return cursor.fetchall()

    def get_proctor(self, proctor_id):
        if not self.is_connected():
            return None
        with self._connection.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM users WHERE id = %s", (proctor_id,))
            return cursor.fetchone()

    def add_proctor(self, proctor_name, email, password):
        if not self.is_connected():
            return False
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        with self._connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO users (proctor_name, email, password, user_role) VALUES (%s, %s, %s, 'proctor')",
                (proctor_name, email, password_hash)
            )
            self._connection.commit()
            return cursor.lastrowid

    def update_proctor(self, proctor_id, proctor_name, email, password):
        if not self.is_connected():
            return False
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        with self._connection.cursor() as cursor:
            cursor.execute(
                "UPDATE users SET proctor_name = %s, email = %s, password = %s, user_role = 'proctor' WHERE id = %s",
                (proctor_name, email, password_hash, proctor_id)
            )
            self._connection.commit()
            return True

    def delete_proctor(self, proctor_id):
        if not self.is_connected():
            return False
        with self._connection.cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE id = %s", (proctor_id,))
            self._connection.commit()
            return True

    def get_reports_for_proctor(self, proctor_id):
        if not self.is_connected():
            return []
        with self._connection.cursor(dictionary=True) as cursor:
            cursor.execute(
                "SELECT * FROM reportlog WHERE user_id = %s ORDER BY date DESC, start DESC",
                (proctor_id,)
            )
            return cursor.fetchall()

    def get_report(self, report_id):
        if not self.is_connected():
            return None
        with self._connection.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM reportlog WHERE id = %s", (report_id,))
            return cursor.fetchone()

    def get_admin(self):
        if not self.is_connected():
            return []
        with self._connection.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM users WHERE user_role = 'admin'")
            return cursor.fetchall()

    def get_roboflow_settings(self):
        if not self.is_connected():
            return None
        with self._connection.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM modelapi ORDER BY id DESC LIMIT 1")
            return cursor.fetchone()

    def update_roboflow_settings(self, api_key, project, model_version, model_classes):
        if not self.is_connected():
            return False
        with self._connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM modelapi"
            )
            cursor.execute(
                "INSERT INTO modelapi (api_key, project, model_version, model_classes) VALUES (%s, %s, %s, %s)",
                (api_key, project, model_version, model_classes)
            )
            self._connection.commit()
            return True
