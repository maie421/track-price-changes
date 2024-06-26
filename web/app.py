import ssl
import sys
from flask import Flask, request, jsonify
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
    return product.getDefulatSearchProduct(request.args.get('keyword'), int(request.args.get('page')))

@app.route("/product/similar", methods=['GET'])
def getSimilarProducts():
    return product.getSimilarProducts(request.args.get('pid'))

@app.route("/v1/search", methods=['GET'])
def getSimilarProduct():
    return product.getAiSearchProduct(request.args.get('keyword'))

if __name__ == "__main__":
    # app.run(ssl_context=context, debug=True)
    app.run()