from flask import Flask
from flask import Response
from flask import json
from flask import request
from sklearn.externals import joblib
import pandas as pd

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict(): 
    json_ = request.json
    dictionary = json_
    link = dictionary["text"]
    #query_df = pd.DataFrame(json_)
    #query = pd.get_dummies(query_df)
    #prediction = clf.predict(query)
    #dict1 = {'prediction': [7, 8, 9]}
    #return Response(dict1, mimetype='application/json')
    return json.dumps([7,8,9])

if __name__ == '__main__':
    check_data = pd.read_csv('check_data.csv')
    linreg = joblib.load('linreg.pkl')
    app.run(port=8080)
