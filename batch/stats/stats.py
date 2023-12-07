import sys
import pandas as pd
from batch.testDbConnect import db_connect_test
from datetime import datetime

conn = db_connect_test()
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
start_time = f"{current_date} 00:00:00"
end_time = f"{current_date} 23:59:59"

df = pd.DataFrame()

for j in modified_numbers:
    sql = "SELECT product_id, price FROM log.products WHERE category_id = %s and created_at > %s and created_at < %s"
    vals = (j, start_time, end_time)
    cur.execute(sql, vals)
    existing_data = cur.fetchall()

    df_temp = pd.DataFrame(existing_data, columns=['product_id', 'price'])
    df_temp_stats = df_temp.groupby('product_id')['price'].agg(['mean', 'min', 'max']).reset_index()
    df_temp_stats.columns = ['product_id', 'mean_price', 'lowest_price', 'highest_price']

cur.close()
conn.close()