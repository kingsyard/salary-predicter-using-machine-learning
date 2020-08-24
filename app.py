import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

import pyrebase

config = {
	"apiKey": "AIzaSyAD6kvrK16x3nnQVQpnybP90YBSjz0X8Og",
  "authDomain": "agriculture-81f5b.firebaseapp.com",
  "databaseURL": "https://agriculture-81f5b.firebaseio.com",
  "projectId": "agriculture-81f5b",
  "storageBucket": "agriculture-81f5b.appspot.com",
  "messagingSenderId": "939998839868",
  "appId": "1:939998839868:web:bdba7971bfd933c1faef39",
  "measurementId": "G-9XLTMEPH2K"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()


app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    int_features = [int(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)
    a1=final_features[0]
    b1=final_features[1]
    c1=final_features[2]
    print(a1,b1,c1)
    db.child("names").push({"score1":a1})
    db.child("names").push({"score2":b1})
    db.child("names").push({"score3":c1})

    output = round(prediction[0], 2)

    return render_template('index.html', prediction_text='Employee Salary should be $ {}'.format(output))


if __name__ == "__main__":
    app.run(debug=True)
