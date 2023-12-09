import pandas as pd
from flask import render_template


class Products:
    def __init__(self, app, db_conn):
        self.app = app
        self.db_conn = db_conn
        self.cursor = db_conn.cursor()

    def index(self):
        try:
            self.cursor.execute("SELECT product_id, price, avg_price FROM track_price_changes.products")
            data = self.cursor.fetchall()
            df = pd.DataFrame(data, columns=['product_id', 'price', 'avg_price'])

            df['discount_rate'] = (df.avg_price - df.price) / df.avg_price * 100

            # # Retrieve the top 12 products based on the discount rate
            top_12_discounted = df.nlargest(12, 'discount_rate')
            # print(top_12_discounted)
            #
            # # Display the result
            print(top_12_discounted[['product_id', 'price', 'avg_price', 'discount_rate']])

            return render_template('index.html', user="반원", data={'level': 60, 'point': 360, 'exp': 45000})
        except Exception as e:
            print(f"Error executing SELECT statement: {e}")
            return None
        finally:
            self.cursor.close()
