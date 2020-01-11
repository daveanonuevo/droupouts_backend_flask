#!flask/bin/python
from flask import Flask, request, jsonify
from predict import predict
import json

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/predict', methods=['POST'])
def get_pred():
    req_data = request.get_json()
    argv = req_data['text']
    fromNumber = req_data['from']
    print(argv)
    x = {"prediction": predict(argv)}
    return predict(argv)


if __name__ == '__main__':
    app.run(debug=True)
