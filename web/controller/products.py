import math
from datetime import datetime, timedelta

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
            df = pd.DataFrame(data, columns=['product_id', 'image', 'name', 'price', 'avg_price'])

            df['discount_rate'] = (df.avg_price - df.price) / df.avg_price * 100

            top_12_discounted = df.nlargest(12, 'discount_rate')

            return render_template('index.html', products=top_12_discounted.to_dict('records'))
        except Exception as e:
            print(f"Error executing SELECT statement: {e}")
        finally:
            if hasattr(cursor, 'closed') and not cursor.closed:
                cursor.close()


    def getProduct(self, pid):
        now_date = datetime.now()
        current_date = now_date.strftime("%Y-%m-%d")

        start_date_format = (now_date - timedelta(days=7)).strftime("%Y-%m-%d")
        start_date = f"{start_date_format} 00:00:00"
        end_date = f"{current_date} 23:59:59"

        cursor = self.db_conn.cursor()
        cursor.execute("SELECT product_id, image, name, price, avg_price FROM track_price_changes.products where product_id = %s", pid)
        product_data = cursor.fetchone()

        discount_rate = (product_data[4] - product_data[3]) / product_data[4] * 100
        increase_rate = (product_data[3] - product_data[4]) / product_data[4] * 100

        cursor.execute("SELECT max(high_price) as high_price, min(low_price) as low_price FROM track_price_changes.products_stats WHERE product_id = %s", pid)
        product_price_data = cursor.fetchone()

        cursor.execute("SELECT high_price,low_price, created_at FROM track_price_changes.products_stats WHERE created_at >= %s AND created_at <= %s and product_id = %s", (start_date, end_date, pid))
        product_stats_data = cursor.fetchall()
        df = pd.DataFrame(product_stats_data, columns=['high_price', 'low_price', 'created_at'])
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
            'increase_rate': increase_rate,
        }, product_stats={df.to_dict('records')})

    def getCategory(self, category_id, paging):
        per_page = 24

        start = (paging - 1) * per_page

        cursor = self.db_conn.cursor()
        category_select_sql = f"SELECT product_id, image, name, price, avg_price FROM track_price_changes.products where category_id = %s limit {per_page} offset {start}"

        cursor.execute(category_select_sql, category_id)
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=['product_id', 'image', 'name', 'price', 'avg_price'])

        df['discount_rate'] = (df.avg_price - df.price) / df.avg_price * 100
        df['increase_rate'] = (df.price - df.avg_price) / df.avg_price * 100

        query = "SELECT count(*) FROM track_price_changes.products where category_id = %s"
        cursor.execute(query, category_id)
        result = cursor.fetchone()

        total_count = result[0]
        page_size = total_count / per_page
        cursor.close()

        return render_template('category.html',
                               products=df.to_dict('records'),
                               page={
                                   'total_count': int(total_count),
                                   'size': math.ceil(page_size)
                               })
