from pyclbr import Function
from pydoc import doc
from flask import Flask, render_template, request, jsonify,session, redirect, url_for,flash
from pymongo import MongoClient

# import bcrypt
import datetime

client = MongoClient('mongodb+srv://test:sparta@cluster0.gfvlmzn.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

app = Flask(__name__)

@app.route('/')
def index():
   if 'username' in session:
    return render_template('index.html')

   return render_template('login.html')

@app.route("/read",methods=["GET"])
def read_data():
    username = session['username']
    sleep_list=list(db.bucket.find({},{'_id':False}))
    return jsonify({'sleep':sleep_list})

@app.route("/create", methods=["POST"])
def create_data():
    # sample_receive = request.form['sample_give']
    mydate = request.form['mydate']
    mytime = request.form['mytime']
    username = session['username']
    # id=int(mydate.replace('-',''))
    
    count = db.bucket.count_documents({})
    id = count + 1
    doc = {
        'id': id,
        'date': mydate,
        'time': mytime,
        'username' : username,
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

@app.route("/delete", methods=["POST"])
def delete_data():
    id_receive = request.form['id_give']    
    db.bucket.delete_one({'id':int(id_receive)})
    return jsonify({'msg':'delete'})

@app.route('/login', methods=['POST'])
def login():
    users = db.users
    login_user = users.find_one({'name' : request.form['username']})

    if login_user:
        if request.form['password'] == login_user['password']:
            session['username'] = request.form['username']
            return redirect(url_for('index'))
    flash('Username or Password not match with our records!')
    return render_template('login.html', error='Invalid credentials')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = db.users
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            users.insert_one({'name' : request.form['username'], 'password' : request.form['password']})
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        
        flash('That username already exists!')
        return render_template('register.html')

    return render_template('register.html')

@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run('0.0.0.0', port=5000, debug=True)
