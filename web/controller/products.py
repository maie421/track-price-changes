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

            top_12_discounted = df.nlargest(12, 'discount_rate')

            print(top_12_discounted)
            return render_template('index.html', products=top_12_discounted.to_dict('records'))
        except Exception as e:
            print(f"Error executing SELECT statement: {e}")
        finally:
            if hasattr(cursor, 'closed') and not cursor.closed:
                cursor.close()


    def getProduct(self, pid):
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT product_id, image, name, price, avg_price FROM track_price_changes.products where product_id = %s", pid)
        product_data = cursor.fetchone()

        discount_rate = (product_data[4] - product_data[3]) / product_data[4] * 100

        cursor.execute("SELECT max(high_price) as high_price, min(low_price) as low_price FROM track_price_changes.products_stats WHERE product_id = %s", pid)
        product_price_data = cursor.fetchone()
        cursor.close()

        return render_template('product.html', product={
            'product_id': product_data[0],
            'image': product_data[1],
            'name': product_data[2],
            'price': product_data[3],
            'avg_price': product_data[4],
            'high_price': product_price_data[0],
            'low_price': product_price_data[1],
            'discount_rate': discount_rate,
        })

    def getCategory(self, category_id, paging):
        per_page = 12

        start = (paging - 1) * per_page
        end = start + per_page

        cursor = self.db_conn.cursor()
        cursor.execute(f"SELECT product_id, image, name, price, avg_price FROM track_price_changes.products where category_id = %s limit {start}, {end}", category_id)
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=['product_id', 'image', 'name', 'price', 'avg_price'])

        df['discount_rate'] = (df.avg_price - df.price) / df.avg_price * 100

        query = "SELECT count(*) FROM track_price_changes.products where category_id = %s"
        cursor.execute(query, category_id)
        result = cursor.fetchone()

        total_count = result[0]
        page_size = total_count % per_page
        cursor.close()

        return render_template('category.html',
                               products=df.to_dict('records'),
                               page={
                                   'total_count': int(total_count),
                                   'size': int(page_size)
                               })
