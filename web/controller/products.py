import math
from datetime import datetime, timedelta

import pandas as pd
from flask import render_template, jsonify

from controller.similarity import compare_images
from testDbConnect import db_connect_test
import itertools


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

            # 할인율이 높은 상품 리스트
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
        cursor.execute(
            "SELECT product_id, image, name, price, avg_price, category_id FROM track_price_changes.products where product_id = %s",
            pid)
        product_data = cursor.fetchone()

        discount_rate = (product_data[4] - product_data[3]) / product_data[4] * 100
        increase_rate = (product_data[3] - product_data[4]) / product_data[4] * 100

        cursor.execute(
            "SELECT max(high_price) as high_price, min(low_price) as low_price FROM track_price_changes.products_stats WHERE product_id = %s",
            pid)
        product_price_data = cursor.fetchone()

        cursor.execute(
            "SELECT high_price, low_price, created_at FROM track_price_changes.products_stats WHERE created_at >= %s AND created_at <= %s and product_id = %s",
            (start_date, end_date, pid))
        product_stats_data = cursor.fetchall()

        # 크롤링된 데이터 날짜
        date_to_index = [row[2].strftime("%Y-%m-%d") for row in product_stats_data]
        # 최근 일주일 날짜
        labels = [(datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(6, -1, -1)]

        # 최근 일주일 기준 존재 하고 있지 않는 크롤링 데이터 확인
        # 해당 상품은 품절 상태
        not_in_labels = []
        for label in labels:
            if label not in date_to_index:
                not_in_labels.append(labels.index(label))

        high_price = [row[0] for row in product_stats_data]
        low_price = [row[1] for row in product_stats_data]

        for i in not_in_labels:
            high_price.insert(i, "")
            low_price.insert(i, "")

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
        }, product_stats={
            'labels': labels,
            'high_price': high_price,
            'low_price': low_price
        })


    def getSimilarProducts(self, pid):
        cursor = self.db_conn.cursor()
        cursor.execute(
            "SELECT product_id, image, name, price, avg_price, category_id FROM track_price_changes.products where product_id = %s",
            pid)
        product_data = cursor.fetchone()

        # 유사 상품
        cursor.execute(
            "SELECT product_id, image, name, price, avg_price, category_id FROM track_price_changes.products WHERE category_id = %s and  product_id != %s",
            (product_data[5], pid))
        _product_category_data = cursor.fetchall()

        specific_image = f'https:{product_data[1]}'

        similarity_scores = {}

        for product_category_data in _product_category_data:
            image_path = f'https:{product_category_data[1]}'
            product_id = product_category_data[0]

            similarity_score = compare_images(specific_image, image_path)

            if 0.6 <= similarity_score < 1.0:
                similarity_scores[product_id] = similarity_score

            if len(similarity_scores) >= 3:
                print("끝남")
                break

        similarity_data = {}
        if len(similarity_scores) > 0:
            keys_only = list(similarity_scores.keys())

            in_clause = ', '.join(['%s'] * len(similarity_scores))
            sql_query = f"SELECT product_id, image, name, price, avg_price, category_id FROM track_price_changes.products WHERE product_id IN ({in_clause})"
            cursor.execute(sql_query, keys_only)
            similarity_data = cursor.fetchall()

        return jsonify(similarity_data)

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

    def getSearchProduct(self, keyword, paging):
        per_page = 24

        start = (paging - 1) * per_page

        cursor = self.db_conn.cursor()
        category_select_sql = f"SELECT product_id, image, name, price, avg_price FROM track_price_changes.products WHERE name LIKE '%{keyword}%' LIMIT {per_page} OFFSET {start}"

        cursor.execute(category_select_sql)
        data = cursor.fetchall()

        df = pd.DataFrame(data, columns=['product_id', 'image', 'name', 'price', 'avg_price'])

        df['discount_rate'] = (df.avg_price - df.price) / df.avg_price * 100
        df['increase_rate'] = (df.price - df.avg_price) / df.avg_price * 100

        query = f"SELECT count(*) FROM track_price_changes.products WHERE name LIKE '%{keyword}%'"
        cursor.execute(query)
        result = cursor.fetchone()

        total_count = result[0]
        page_size = total_count / per_page
        cursor.close()

        return render_template('search.html',
                               products=df.to_dict('records'),
                               page={
                                   'total_count': int(total_count),
                                   'size': math.ceil(page_size)
                               })
