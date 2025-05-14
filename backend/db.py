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
            return False, "Database not connected"
        try:
            with self._connection.cursor() as cursor:
                # Start transaction
                self._connection.start_transaction()
                
                # Get report count first for verification
                cursor.execute("SELECT COUNT(*) FROM reportlog WHERE user_id = %s", (proctor_id,))
                report_count = cursor.fetchone()[0]
                
                # Perform deletion (CASCADE will handle reports)
                cursor.execute("DELETE FROM users WHERE id = %s", (proctor_id,))
                if cursor.rowcount == 0:
                    self._connection.rollback()
                    return False, "Proctor not found"
                
                self._connection.commit()
                return True, f"{report_count} reports deleted"
                
        except Error as e:
            self._connection.rollback()
            print(f"MySQL Error [{e.errno}]: {e.msg}")  # Detailed error logging
            return False, f"Database error: {str(e)}"

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
