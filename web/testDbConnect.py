import pymysql

def db_connect_test():
    conn = pymysql.connect(host='49.247.174.57', user='batch', password='track', charset='utf8')

    return conn