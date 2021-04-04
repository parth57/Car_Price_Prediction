from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('regression_rf.pkl', 'rb'))
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():

    if request.method == 'POST':
        Year = int(request.form['Year'])
        Year = 2021 - Year
        Present_Price = float(request.form['Present_Price'])
        Kms_Driven = int(request.form['Kms_Driven'])
        Kms_Driven2 = np.log(Kms_Driven)
        Owner = int(request.form['Owner'])
        Fuel_Type = request.form['Fuel_Type']
        if (Fuel_Type == 'Petrol'):
            Fuel_Type = 239

        elif (Fuel_Type == 'Diesel'):
            Fuel_Type = 60

        else:
            Fuel_Type = 2
        Seller_Type = request.form['Seller_Type']
        if (Seller_Type == 'Individual'):
            Seller_Type = 106

        else:
            Seller_Type = 195

        Transmission = request.form['Transmission']
        if(Transmission == 'Mannual'):
            Transmission = 261
        else:
            Transmission = 40
        prediction = model.predict([[Present_Price,Kms_Driven2,Fuel_Type,Seller_Type,Transmission,Owner,Year]])
        output = round(prediction[0],2)
        if output<0:
            return render_template('index.html',prediction_texts = "Sorry you cannot sell this car")
        else:
            return render_template('index.html',prediction_text = f"You Can Sell The Car at {output}")
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)

