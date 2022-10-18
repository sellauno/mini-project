from pydoc import doc
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import datetime

client = MongoClient('mongodb+srv://test:sparta@cluster0.gfvlmzn.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

app = Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')

@app.route("/read",methods=["GET"])
def read_data():
    sleep_list=list(db.bucket.find({},{'_id':False}))
    return jsonify({'sleep':sleep_list})

@app.route("/create", methods=["POST"])
def create_data():
    # sample_receive = request.form['sample_give']
    mydate = request.form['mydate']
    mytime = request.form['mytime']

    num = datetime.datetime.now()
    num.isoformat()

    doc = {
        'num': num,
        'date': mydate,
        'time': mytime,
    }
    db.bucket.insert_one(doc)
    return jsonify({'msg': 'data saved!'})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)
