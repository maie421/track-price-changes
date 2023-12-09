import sys
from flask import Flask
from web.dbConnect import db_connect
from web.controller.products import Products

# Flask 객체 인스턴스 생성
app = Flask(__name__)
db_connection = db_connect(sys)

product = Products(app, db_connect)

@app.route('/')  # 접속하는 url
def index():
    return product.index()


if __name__ == "__main__":
    app.run()
    # app.run(port=80, debug=True)
