#!flask/bin/python
from flask import Flask, request, jsonify
from predict import predict
import json
import psycopg2

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
    return x


@app.route('/report', methods=['POST'])
def report_user():
    req_data = request.get_json()
    message = req_data['text']
    fromNumber = req_data['from']
    try:
        conn = psycopg2.connect(dbname='defaultdb', user='doadmin', host='db-postgresql-sgp1-98876-do-user-6642548-0.db.ondigitalocean.com',
                                password='h3pv5gg36ctgnzq9', port=25060, sslmode="require")
        curs = conn.cursor()
        curs.execute(
            "INSERT INTO public.reports(from_number,reported_message) VALUES (%s, %s)", (fromNumber, message))
        conn.commit()
        curs.close()
        return(":)")
    except:
        print("I am unable to connect to the database")
        return(":(")


@app.route('/admin')
def get_reports():
    try:
        conn = psycopg2.connect(dbname='defaultdb', user='doadmin', host='db-postgresql-sgp1-98876-do-user-6642548-0.db.ondigitalocean.com',
                                password='h3pv5gg36ctgnzq9', port=25060, sslmode="require")
        curs = conn.cursor()
        curs.execute(
            "SELECT from_number, reported_message, COUNT(*) FROM public.reports GROUP BY from_number, reported_message HAVING count(from_number) > 3")
        records = curs.fetchmany(3)
        print(records)
        records = json.dumps(records)
        curs.close()
        return(records)
    except:
        print("I am unable to connect to the database")
        return(":(")


if __name__ == '__main__':
    app.run(debug=False)
