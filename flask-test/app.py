import pickle
from flask import Flask, render_template, request
import pandas as pd
import json


app = Flask(__name__)

# Load the trained model into memory
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

import pandas as pd

# Define a function for preprocessing the input data
def preprocess(input_data):
    # Create a DataFrame from the input data
    input_df = pd.DataFrame(input_data, columns=['idade', 'genero', 'estado_civil'])

    # One-hot encode the categorical features
    input_df_encoded = pd.get_dummies(input_df, columns=['genero', 'estado_civil'])

    # Return the preprocessed data as a numpy array
    return input_df_encoded.values


# Define a new route for handling predictions
@app.route('/predict', methods=['POST'])
def predict():
    # Get the input data from the request
    idade = int(request.form['idade'])
    genero = request.form['genero']
    estado_civil = request.form['estado_civil']

    # Preprocess the input data (one-hot encoding)
    input_data = {'idade': [idade], 'genero': [genero], 'estado_civil': [estado_civil]}
    input_df = pd.DataFrame(input_data)
    input_df['genero_Feminino'] = (input_df['genero'] == 'Feminino').astype(int)
    input_df['genero_Masculino'] = (input_df['genero'] == 'Masculino').astype(int)
    input_df.drop('genero', axis=1, inplace=True)
    estado_civil_categories = ['Casado (a)', 'Divorciado (a)', 'Nao respondeu', 'Outro', 'Solteiro (a)', 'Viuvo (a)']
    input_df['estado_civil'] = pd.Categorical(input_df['estado_civil'], categories=estado_civil_categories)
    input_df_preprocessed = pd.get_dummies(input_df, columns=['estado_civil'])

    # Use the model to make a prediction
    prediction = model.predict(input_df_preprocessed)[0]

    # Return the prediction as a JSON object
    response = {'prediction': prediction}
    return json.dumps(response)


# Define the index route (with a form for entering input data)
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
