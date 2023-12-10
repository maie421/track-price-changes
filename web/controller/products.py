import pandas as pd
from flask import render_template

from testDbConnect import db_connect_test
# from dbConnect import db_connect


class Products:
    def __init__(self, app):
        self.app = app
        self.db_conn = db_connect_test()

    def index(self):
        try:
            cursor = self.db_conn.cursor()
            cursor.execute("SELECT product_id, image, name, price, avg_price FROM track_price_changes.products;")
            data = cursor.fetchall()
            df = pd.DataFrame(data, columns=['product_id','image','name', 'price', 'avg_price'])

            df['discount_rate'] = (df.avg_price - df.price) / df.avg_price * 100

            # # Retrieve the top 12 products based on the discount rate
            top_12_discounted = df.nlargest(12, 'discount_rate')
            # print(top_12_discounted)
            #
            # # Display the result
            # print(top_12_discounted[['product_id', 'price', 'avg_price', 'discount_rate']])
            print(top_12_discounted)
            return render_template('index.html', products=top_12_discounted.to_dict('records'))
        except Exception as e:
            print(f"Error executing SELECT statement: {e}")
            # You might want to log the exception or handle it appropriately
            # For now, returning a simple error response
            # return render_template('error.html', error_message=str(e))
        finally:
            if hasattr(cursor, 'closed') and not cursor.closed:
                cursor.close()


    def getProduct(self):
        return render_template('product.html')