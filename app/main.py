import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import requests
from io import StringIO
from flask import Flask
from flask import request
import json

def crear_app():

    app = Flask(__name__)

    @app.route("/")
    def index():
        return "hello world!"

    @app.route("/uf")
    def uf():
        anio = request.args.get("anio")
        mes = request.args.get("mes")
        # Descargar el archivo CSV desde el enlace
        url = "https://raw.githubusercontent.com/NicoMonc/DataScience/main/uf.csv"
        response = requests.get(url)

        # Comprobar si la descarga fue exitosa
        if response.status_code == 200:
            # Leer el contenido del CSV
            csv_data = response.text
            # Crear un objeto StringIO para que pandas pueda leer el CSV desde una cadena
            csv_io = StringIO(csv_data)

            # Cargar el CSV en un DataFrame
            data = pd.read_csv(csv_io)

            # Preparar los datos
            X = data[["Año", "Mes"]]
            y = data["Valor"]

            # Crear un objeto de regresión lineal y entrenar el modelo
            model = LinearRegression()
            model.fit(X, y)
            
            # Predecir el valor de la UF para el año y mes indicado
            año = int(anio)
            mes = int(mes)
            valor = model.predict([[año, mes]])
            return json.dumps({"valor": valor[0]})

    return app