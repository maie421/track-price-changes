import sys
from flask import Flask
from controller.products import Products
# Flask 객체 인스턴스 생성
app = Flask(__name__)
# db_connection = db_connect(sys)

product = Products(app)
@app.route('/')
def index():
    return product.index()


if __name__ == "__main__":
    app.run()
    # app.run(port=80, debug=True)
