import pymysql

def db_connect_test():
    conn = pymysql.connect(host='', user='', password='', charset='utf8')

    return conn
