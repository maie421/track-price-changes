import sys
import pymysql
import pandas as pd
from datetime import datetime, timedelta

if len(sys.argv) >= 4:
    host = str(sys.argv[1])
    user = str(sys.argv[2])
    password = str(sys.argv[3])

    conn = pymysql.connect(host=host, user=user, password=password, db='log', charset='utf8')
else:
    print("Usage: python script.py <host> <user> <password>")

# conn = db_connect_test()

# pymysql 로그 활성화
# pymysql_logger = logging.getLogger('pymysql')
# pymysql_logger.setLevel(logging.DEBUG)
# pymysql_logger.addHandler(logging.StreamHandler())

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
category_numbers = {502483, 502484, 502485, 502486, 502487, 502489, 502490, 502491}
# original_numbers = {502483}

modified_numbers = {str(num)[:3] + '3' + str(num)[4:] for num in category_numbers}

now_date = datetime.now()
current_date = now_date.strftime("%Y-%m-%d")
start_date = f"{current_date} 00:00:00"
end_date = f"{current_date} 23:59:59"

start_date_7_days_ago_format = (now_date - timedelta(days=7)).strftime("%Y-%m-%d")
start_date_7_days_ago = f"{start_date_7_days_ago_format} 00:00:00"


df = pd.DataFrame()

for j in modified_numbers:
    sql = "SELECT product_id, price FROM log.products WHERE category_id = %s and created_at > %s and created_at < %s"
    vals = (j, start_date, end_date)
    cur.execute(sql, vals)
    existing_data = cur.fetchall()
    print(existing_data)

    df_temp = pd.DataFrame(existing_data, columns=['product_id', 'price'])
    df_temp_stats = df_temp.groupby('product_id')['price'].agg(['max', 'min', 'mean']).reset_index()
    df_temp_stats.columns = ['product_id', 'high_price', 'low_price', 'avg_price']
    print(df_temp_stats)

    for index, row in df_temp_stats.iterrows():
        product_id = row['product_id']
        high_price = row['high_price']
        low_price = row['low_price']
        avg_price = row['avg_price']

        cur.execute(
            f"SELECT id FROM track_price_changes.products_stats WHERE product_id = {product_id} and created_at >= '{start_date}' AND created_at <= '{end_date}'")

        existing_data = cur.fetchone()
        if existing_data:
            update_query = f"UPDATE track_price_changes.products_stats SET high_price = {high_price}, " \
                           f"low_price = {low_price}, avg_price = {avg_price} WHERE id = {existing_data[0]}"
            print("update : ", update_query)
            cur.execute(update_query)
        else:
            insert_query = f"INSERT INTO track_price_changes.products_stats (product_id, high_price, low_price, avg_price) " \
                           f"VALUES ({product_id}, {high_price}, {low_price}, {avg_price})"
            print("insert : ", insert_query)
            cur.execute(insert_query)

        conn.commit()

    select_sql_query = """
            SELECT p.product_id, p.price, name, image, category_id
            FROM log.products p
            JOIN (
                SELECT product_id, MAX(created_at) AS max_created_at
                FROM log.products
                WHERE category_id = %s
                AND created_at >= %s AND created_at <= %s
                GROUP BY product_id
            ) AS max_dates
            ON p.product_id = max_dates.product_id AND p.created_at = max_dates.max_created_at
            WHERE p.category_id = %s
            AND created_at >= %s AND created_at <= %s
        """
    cur.execute(select_sql_query, (j, start_date, end_date, j, start_date, end_date))

    # 결과 가져오기
    data = cur.fetchall()

    # 결과 출력
    for item in data:
        try:
            select_sql_query = f"""
                    SELECT product_id, AVG(avg_price) AS avg_price
                    FROM track_price_changes.products_stats
                    WHERE created_at >= '{start_date_7_days_ago}'
                      AND created_at <= '{end_date}'
                      AND product_id = '{item[0]}'
                """
            print(select_sql_query)
            cur.execute(select_sql_query)
            result = cur.fetchone()

            item = item + (result[1],)

            sql_query = """
                    INSERT IGNORE INTO track_price_changes.products (product_id, price, name, image, category_id, avg_price)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                        price = VALUES(price),
                        name = VALUES(name),
                        image = VALUES(image),
                        category_id = VALUES(category_id),
                        avg_price = VALUES(avg_price)
                """
            cur.execute(sql_query, item)
            conn.commit()

        except Exception as e:
            print(f"Error: {e}")

        # 확인을 위해 rowcount 출력
        print(f"Rowcount for {item}: {cur.rowcount}")

cur.close()
conn.close()
