import pickle
from flask import Flask, render_template, request
import pandas as pd
import json
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)

# Load the trained model into memory
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

# Define a label encoder to convert categorical features into numeric features
le = LabelEncoder()

# Define a function for preprocessing the input data
def preprocess(input_data):
    # Create a DataFrame from the input data
    input_df = pd.DataFrame(input_data, columns=['idade', 'genero', 'estado_civil', 'faixa_renda'])

    # Convert categorical features into numeric features using label encoding
    input_df['genero'] = input_df['genero'].apply(lambda x: 1 if x == 'Feminino' else 0)
    estado_civil_categories = ['Solteiro (a)', 'Casado (a)', 'Outro', 'Divorciado (a)', 'Viuvo (a)']
    input_df['estado_civil'] = pd.Categorical(input_df['estado_civil'], categories=estado_civil_categories).codes
    faixa_renda_categories = ['Até um salário mínimo (R$ 954,00)', 'De 1 a 2 salários (R$ 954,00 - R$ 1.908,00)',
                             'De 2 a 4 salários (R$ 1.875,00 - R$ 3.816,00)', 'De 4 a 8 salários (R$ 3.749,00 - R$ 7.632,00)',
                             'Acima de 8 salários (acima de R$ 7.632,00)']
    input_df['faixa_renda'] = pd.Categorical(input_df['faixa_renda'], categories=faixa_renda_categories).codes

    # Return the preprocessed data as a numpy array
    return input_df.values

# Define a new route for handling predictions
@app.route('/predict', methods=['POST'])
def predict():
    # Get the input data from the request
    idade = int(request.form['idade'])
    genero = request.form['genero']
    estado_civil = request.form['estado_civil']
    faixa_renda = request.form['faixa_renda']

    # Preprocess the input data
    input_data = {'idade': [idade], 'genero': [genero], 'estado_civil': [estado_civil], 'faixa_renda': [faixa_renda]}
    input_data_preprocessed = preprocess(input_data)

    # Use the model to make a prediction
    prediction = model.predict(input_data_preprocessed)[0]
    prediction_list = prediction.tolist()

    # Return the prediction as a JSON object
    response = {'prediction': prediction_list}
    return json.dumps(response)


# Define the index route (with a form for entering input data)
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
