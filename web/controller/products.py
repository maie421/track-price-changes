from flask import render_template


class Products:
    def __init__(self, app, db_conn):
        self.app = app
        self.db_conn = db_conn

    def index(self):
        try:
            cursor = self.db_conn.cursor()
            cursor.execute("SELECT * FROM your_table")
            result = cursor.fetchall()
            # Process the result as needed
            return render_template('index.html', product=result)
        except Exception as e:
            print(f"Error executing SELECT statement: {e}")
            return None
        finally:
            cursor.close()
