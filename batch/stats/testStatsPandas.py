import sys
import pandas as pd
from batch.testDbConnect import db_connect_test
from datetime import datetime, timedelta
import logging

conn = db_connect_test()

# pymysql 로그 활성화
# pymysql_logger = logging.getLogger('pymysql')
# pymysql_logger.setLevel(logging.DEBUG)
# pymysql_logger.addHandler(logging.StreamHandler())

# SQLAlchemy 로그 활성화
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)

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

# current_date = datetime.now().strftime("%Y-%m-%d")
# start_time = f"{current_date} 00:00:00"
# end_time = f"{current_date} 23:59:59"

current_date_time = datetime.now()

# Subtract one day
one_day_ago = current_date_time - timedelta(days=1)

# Format the result as a string in the desired format
one_day_ago_str = one_day_ago.strftime("%Y-%m-%d")

# Update start_time and end_time
start_time = f"{one_day_ago_str} 00:00:00"
end_time = f"{one_day_ago_str} 23:59:59"


df = pd.DataFrame()

for j in modified_numbers:
    sql = "SELECT product_id, price FROM log.products WHERE category_id = %s and created_at > %s and created_at < %s"
    vals = (j, start_time, end_time)
    cur.execute(sql, vals)
    existing_data = cur.fetchall()

    df_temp = pd.DataFrame(existing_data, columns=['product_id', 'price'])
    df_temp_stats = df_temp.groupby('product_id')['price'].agg(['max', 'min', 'mean']).reset_index()
    df_temp_stats.columns = ['product_id', 'high_price', 'low_price', 'age_price']
    print(df_temp_stats)

    chunk_size = 250

    for i in range(0, len(df_temp_stats), chunk_size):
        chunk = df_temp_stats.iloc[i:i + chunk_size]

        # Update existing records in batches
        update_query = """
        UPDATE track_price_changes.products_stats AS t
        SET 
            t.high_price = s.high_price,
            t.low_price = s.low_price,
            t.age_price = s.age_price
        WHERE t.product_id = s.product_id AND (created_at > %s AND created_at < %s);
        """
        update_query = update_query.replace(":table_name", "%s")
        with conn.cursor() as cursor:
            print(update_query)
            for _, row in chunk.iterrows():
                cursor.execute(update_query, (int(row['high_price']), int(row['low_price']), float(row['age_price']), int(row['product_id']),start_time, end_time))

        # Insert new records in batches
        insert_query = """
        INSERT INTO track_price_changes.products_stats (product_id, high_price, low_price, age_price)
        SELECT 
            s.product_id,
            s.high_price,
            s.low_price,
            s.age_price,
        WHERE NOT EXISTS (
            SELECT 1
            FROM track_price_changes.products_stats AS t
            WHERE t.product_id = s.product_id AND (created_at > %s AND created_at < %s)
        );
        """
        insert_query = insert_query.replace(":table_name", "%s")
        with conn.cursor() as cursor:
            print(insert_query)
            for _, row in chunk.iterrows():
                cursor.execute(insert_query, int(row['product_id']), int(row['high_price']), int(row['low_price']), float(row['age_price']),start_time, end_time)

        conn.commit()
cur.close()
conn.close()