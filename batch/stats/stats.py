import sys
import pandas as pd
from sqlalchemy import create_engine
from batch.testDbConnect import db_connect_test
from datetime import datetime, timedelta
import logging

conn = db_connect_test()

# pymysql 로그 활성화
pymysql_logger = logging.getLogger('pymysql')
pymysql_logger.setLevel(logging.DEBUG)
pymysql_logger.addHandler(logging.StreamHandler())

# SQLAlchemy 로그 활성화
# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)

cur = conn.cursor()

# 502483 : "국/탕/전골"
# 502484 : "덮밥/비빔밥"
# 502485 : "스테이크/고기"
# 502486 : "면/파스타/감바스"
# 502487 : "분식"
# 502489 : "어린이 만들기 겸용"
# 502490 : "중식요리"
# 502491 : "기타요리"
# original_numbers = {502483, 502484, 502485, 502486, 502487, 502489, 502490, 502491}
original_numbers = {502483}

modified_numbers = {str(num)[:3] + '3' + str(num)[4:] for num in original_numbers}

current_date = datetime.now().strftime("%Y-%m-%d")
start_date = f"{current_date} 00:00:00"
end_date = f"{current_date} 23:59:59"

df = pd.DataFrame()

for j in modified_numbers:
    sql = "SELECT product_id, price FROM log.products WHERE category_id = %s and created_at > %s and created_at < %s"
    vals = (j, start_date, end_date)
    cur.execute(sql, vals)
    existing_data = cur.fetchall()

    df_temp = pd.DataFrame(existing_data, columns=['product_id', 'price'])
    df_temp_stats = df_temp.groupby('product_id')['price'].agg(['max', 'min', 'mean']).reset_index()
    df_temp_stats.columns = ['product_id', 'high_price', 'low_price', 'avg_price']
    print(df_temp_stats)

    for index, row in df_temp_stats.iterrows():
        product_id = row['product_id']
        high_price = row['high_price']
        low_price = row['low_price']
        avg_price = row['avg_price']

        # Check if the product_id already exists in the table
        cur.execute(
            f"SELECT id FROM track_price_changes.products_stats WHERE created_at >= '{start_date}' AND created_at <= '{end_date}' and product_id = {product_id}")

        existing_data = cur.fetchone()
        if existing_data:
            # If product_id exists, update the existing row
            update_query = f"UPDATE track_price_changes.products_stats SET high_price = {high_price}, " \
                           f"low_price = {low_price}, avg_price = {avg_price} WHERE id = {existing_data[0]}"
            print("update : ", update_query)
            cur.execute(update_query)
        else:
            # If product_id does not exist, insert a new row
            insert_query = f"INSERT INTO track_price_changes.products_stats (product_id, high_price, low_price, avg_price) " \
                           f"VALUES ({product_id}, {high_price}, {low_price}, {avg_price})"
            print("insert : ", insert_query)
            cur.execute(insert_query)

        conn.commit()
cur.close()
conn.close()
