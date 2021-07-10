from pywebio.platform.flask import webio_view
from pywebio import STATIC_PATH
from flask import Flask, send_from_directory
from pywebio.input import *
from pywebio.output import *

import pickle
import numpy as np
import os


target = 'random_forest_regression_model.pkl'
open(target, 'a').close()
model = {} # model is an empty dict already

if os.path.getsize(target) > 0:      
    with open(target, "rb") as f:
        unpickler = pickle.Unpickler(f)
        # if file is not empty model will be equal
        # to the value unpickled
        model = unpickler.load()

app = Flask(__name__)

def predict():
    Year = input("Enter the Model Year：", type=NUMBER)
    Year = 2021 - Year
    Present_Price = input("Enter the Present Price(in LAKHS)", type=FLOAT)
    Kms_Driven = input("Enter the distance it has travelled(in KMS)：", type=FLOAT)
    Kms_Driven2 = np.log(Kms_Driven)
    Owner = input("Enter the number of owners who have previously owned it(0 or 1 or 2 or 3)", type=NUMBER)
    Fuel_Type = select('What is the Fuel Type', ['Petrol', 'Diesel','CNG'])
    if (Fuel_Type == 'Petrol'):
        Fuel_Type_Petrol = 1
        Fuel_Type_Diesel = 0

    elif (Fuel_Type == 'Diesel'):
        Fuel_Type_Petrol = 0
        Fuel_Type_Diesel = 1

    else:
        Fuel_Type_Petrol = 0
        Fuel_Type_Diesel = 0
    Seller_Type = select('Are you a dealer or an individual', ['Dealer', 'Individual'])
    if (Seller_Type == 'Individual'):
        Seller_Type_Individual = 1
    else:
        Seller_Type_Individual = 0
    Transmission = select('Transmission Type', ['Manual Car', 'Automatic Car'])
    if (Transmission == 'Manual Car'):
        Transmission_Manual = 1
    else:
        Transmission_Manual = 0
    prediction = model.predict([[Present_Price, Kms_Driven, Owner, Year, Fuel_Type_Diesel, Fuel_Type_Petrol, Seller_Type_Individual, Transmission_Manual]])
    output = round(prediction[0], 2)
    print(output)

    if output < 0:
        print("Sorry You can't sell this Car")
        put_text("Sorry You can't sell this Car")

    else:
        print('You can sell this Car at price:')
        put_text('You can sell this Car at price:',output)

app.add_url_rule('/tool', 'webio_view', webio_view(predict),
            methods=['GET', 'POST', 'OPTIONS'])

PORT = int(os.environ.get('PORT', 5000))
app.run(host='localhost', port=PORT)
