from flask import Flask, jsonify, request, send_file
import plotly.graph_objs as go
import pandas as pd
import io
import os
import redis

app = Flask(__name__)

from flask import Flask
from flask_cors import CORS  # Importa la extensión CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:80"}})  # Reemplaza con la URL de tu aplicación React en producción

# Resto de tu código Flask


# Configuración de la conexión a Redis desde la variable de entorno o una URL predeterminada

@app.route('/', methods=['GET', 'POST'])
def upload_form():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            # Aquí puedes procesar el archivo si es necesario
            return upload()

    return '''
    <!doctype html>
    <title>Subir archivo CSV</title>
    <h1>Subir archivo CSV</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"})

    if file:
        # Cargar el archivo CSV en un DataFrame de pandas
        ratings = pd.read_csv(file)

        # Crear la gráfica Plotly
        data = ratings.groupby('userId')['rating'].count().clip(upper=80)

        # Crear trace
        trace = go.Histogram(x=data.values,
                            name='Ratings',
                            xbins=dict(start=0, end=50, size=2))

        # Crear layout
        layout = go.Layout(title='Distribution Of Number of Ratings Per User (Clipped at 50)',
                           xaxis=dict(title='Number of Ratings Per User'),
                           yaxis=dict(title='Count'),
                           bargap=0.2)

        # Crear plot
        fig = go.Figure(data=[trace], layout=layout)

        # Guardar la figura como imagen en Redis
        img_binary = fig.to_image(format='png')
        # Retornar el contenido binario de la imagen y su tipo MIME
        return send_file(io.BytesIO(img_binary), mimetype='image/png')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)