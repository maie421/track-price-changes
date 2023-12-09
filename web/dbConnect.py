import pymysql

def db_connect(sys):
    conn = ""
    if len(sys.argv) >= 4:
        host = str(sys.argv[1])
        user = str(sys.argv[2])
        password = str(sys.argv[3])

        conn = pymysql.connect(host=host, user=user, password=password, db='log', charset='utf8')
    else:
        print("Usage: python script.py <host> <user> <password>")

    return conn
