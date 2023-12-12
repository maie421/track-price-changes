import ssl
import sys
from flask import Flask, request
from controller.products import Products
# Flask 객체 인스턴스 생성
app = Flask(__name__)
# db_connection = db_connect(sys)

product = Products(app)
@app.route('/')
def index():
    return product.index()

@app.route('/product', methods=['GET'])
def getProduct():
    return product.getProduct(request.args.get('pid'))

@app.route('/category', methods=['GET'])
def getCategory():
    return product.getCategory(request.args.get('cat'), int(request.args.get('page')))

@app.route('/search', methods=['GET'])
def getSearchProduct():
    return product.getSearchProduct(request.args.get('keyword'), int(request.args.get('page')))

if __name__ == "__main__":
    # context = ('cert.pem', 'key.pem')
    # app.run(ssl_context=context, debug=True)
    app.run(ssl_context=('cert.crt', 'key.key'))