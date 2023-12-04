from flask import Flask, render_template

# Flask 객체 인스턴스 생성
app = Flask(__name__)


@app.route('/')  # 접속하는 url
def index():
    return render_template('index.html', user="반원", data={'level': 60, 'point': 360, 'exp': 45000})


if __name__ == "__main__":
    # app.run(debug=True)
    app.run(port=80, debug=True)
