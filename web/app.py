import sys
from flask import Flask
from dbConnect import db_connect
from controller.products import Products
from testDbConnect import db_connect_test
# Flask 객체 인스턴스 생성
app = Flask(__name__)
# db_connection = db_connect(sys)
db_connect = db_connect_test()

product = Products(app, db_connect)

@app.route('/')
def index():
    return product.index()


if __name__ == "__main__":
    app.run()
    # app.run(port=80, debug=True)
