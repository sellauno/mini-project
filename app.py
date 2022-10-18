from pyclbr import Function
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
    count = db.bucket.count_documents({})
    id = count + 1

    num = datetime.datetime.now()
    num.isoformat()

    doc = {
        'id': id,
        'num': num,
        'date': mydate,
        'time': mytime,
    }
    db.bucket.insert_one(doc)
    return jsonify({'msg': 'data saved!'})

# Update Function
@app.route('/update', methods=["POST"])
def update_data():
    id_receive = request.form['id_give']
    date_receive = request.form['date_give']
    time_receive = request.form['time_give']
    db.bucket.update_one(
        {'id': int(id_receive)},
        {'$set': {'date': date_receive,'time': time_receive}}
        )
    return jsonify({'msg': 'POST /bucket/done request!'})


if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)
