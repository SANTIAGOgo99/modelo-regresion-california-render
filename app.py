from flask import Flask, request, jsonify, render_template_string
import joblib
import pandas as pd

app = Flask(__name__)

# Cargar modelo entrenado
modelo = joblib.load("modelo_regresion_california.pkl")

HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Estimador de Valor de Viviendas</title>
    <style>
        * {
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            margin: 0;
            min-height: 100vh;
            background: linear-gradient(135deg, #e8f0ff, #fdf2f8);
            color: #1e293b;
        }

        .pagina {
            max-width: 1180px;
            margin: 0 auto;
            padding: 35px 20px;
        }

        .encabezado {
            text-align: center;
            margin-bottom: 30px;
        }

        .encabezado h1 {
            font-size: 46px;
            margin: 0;
            color: #312e81;
        }

        .encabezado p {
            font-size: 17px;
            color: #475569;
            margin-top: 10px;
        }

        .tarjeta-principal {
            display: grid;
            grid-template-columns: 2fr 0.9fr;
            gap: 25px;
            align-items: start;
        }

        .formulario {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 22px;
            padding: 28px;
            box-shadow: 0 18px 45px rgba(49, 46, 129, 0.15);
            border: 1px solid #e0e7ff;
        }

        .seccion-titulo {
            font-size: 22px;
            margin-bottom: 20px;
            color: #312e81;
            font-weight: 700;
        }

        .grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 18px;
        }

        .campo {
            display: flex;
            flex-direction: column;
        }

        label {
            font-weight: 700;
            color: #334155;
            margin-bottom: 6px;
        }

        .ayuda {
            font-size: 13px;
            color: #64748b;
            margin-bottom: 7px;
            line-height: 1.3;
        }

        input, select {
            padding: 13px 14px;
            border-radius: 12px;
            border: 1px solid #cbd5e1;
            font-size: 15px;
            background: #f8fafc;
            color: #0f172a;
            outline: none;
            transition: 0.2s;
        }

        input:focus, select:focus {
            border-color: #7c3aed;
            box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.15);
            background: #ffffff;
        }

        .boton {
            margin-top: 25px;
            width: 100%;
            padding: 16px;
            border: none;
            border-radius: 14px;
            background: linear-gradient(135deg, #7c3aed, #2563eb);
            color: white;
            font-weight: 800;
            font-size: 16px;
            cursor: pointer;
            transition: 0.2s;
        }

        .boton:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 25px rgba(37, 99, 235, 0.25);
        }

        .resultado {
            background: #111827;
            color: white;
            border-radius: 22px;
            padding: 28px;
            box-shadow: 0 18px 45px rgba(17, 24, 39, 0.22);
            position: sticky;
            top: 25px;
        }

        .resultado h2 {
            margin-top: 0;
            font-size: 24px;
            color: #c4b5fd;
        }

        .precio {
            font-size: 38px;
            font-weight: 900;
            margin: 20px 0;
            color: #ffffff;
        }

        .texto-resultado {
            color: #d1d5db;
            font-size: 15px;
            line-height: 1.5;
        }

        .badge {
            display: inline-block;
            background: #312e81;
            color: #ddd6fe;
            padding: 7px 12px;
            border-radius: 999px;
            font-size: 13px;
            margin-bottom: 15px;
        }

        .nota {
            margin-top: 22px;
            background: #eef2ff;
            border-left: 5px solid #7c3aed;
            padding: 14px;
            border-radius: 12px;
            font-size: 14px;
            color: #475569;
            line-height: 1.5;
        }

        @media (max-width: 900px) {
            .tarjeta-principal {
                grid-template-columns: 1fr;
            }

            .grid {
                grid-template-columns: 1fr;
            }

            .encabezado h1 {
                font-size: 34px;
            }

            .resultado {
                position: static;
            }
        }
    </style>
</head>
<body>
    <div class="pagina">
        <div class="encabezado">
            <h1>Estimador de Valor de Viviendas</h1>
            <p>Modelo de regresión entrenado con el dataset California Housing</p>
        </div>

        <div class="tarjeta-principal">
            <div class="formulario">
                <div class="seccion-titulo">Datos de entrada</div>

                <form method="POST" action="/">
                    <div class="grid">

                        <div class="campo">
                            <label>Longitud geográfica</label>
                            <span class="ayuda">Ejemplo: -122.23. Representa la ubicación este-oeste de la zona.</span>
                            <input type="number" step="any" name="longitude" value="{{ datos.longitude }}" required>
                        </div>

                        <div class="campo">
                            <label>Latitud geográfica</label>
                            <span class="ayuda">Ejemplo: 37.88. Representa la ubicación norte-sur de la zona.</span>
                            <input type="number" step="any" name="latitude" value="{{ datos.latitude }}" required>
                        </div>

                        <div class="campo">
                            <label>Edad media de las viviendas</label>
                            <span class="ayuda">Ejemplo: 41. Indica la edad promedio de las casas de la zona.</span>
                            <input type="number" step="any" name="housing_median_age" value="{{ datos.housing_median_age }}" required>
                        </div>

                        <div class="campo">
                            <label>Total de habitaciones</label>
                            <span class="ayuda">Ejemplo: 880. Total de habitaciones registradas en el área.</span>
                            <input type="number" step="any" name="total_rooms" value="{{ datos.total_rooms }}" required>
                        </div>

                        <div class="campo">
                            <label>Total de dormitorios</label>
                            <span class="ayuda">Ejemplo: 129. Total de dormitorios registrados en la zona.</span>
                            <input type="number" step="any" name="total_bedrooms" value="{{ datos.total_bedrooms }}" required>
                        </div>

                        <div class="campo">
                            <label>Población</label>
                            <span class="ayuda">Ejemplo: 322. Cantidad aproximada de personas en la zona.</span>
                            <input type="number" step="any" name="population" value="{{ datos.population }}" required>
                        </div>

                        <div class="campo">
                            <label>Hogares</label>
                            <span class="ayuda">Ejemplo: 126. Número de hogares o viviendas habitadas.</span>
                            <input type="number" step="any" name="households" value="{{ datos.households }}" required>
                        </div>

                        <div class="campo">
                            <label>Ingreso medio</label>
                            <span class="ayuda">Ejemplo: 8.3252. Representa el ingreso medio de la zona.</span>
                            <input type="number" step="any" name="median_income" value="{{ datos.median_income }}" required>
                        </div>

                        <div class="campo">
                            <label>Proximidad al océano</label>
                            <span class="ayuda">Ejemplo: Cerca de la bahía. Selecciona la ubicación respecto al océano.</span>
                            <select name="ocean_proximity" required>
                                <option value="NEAR BAY" {% if datos.ocean_proximity == "NEAR BAY" %}selected{% endif %}>Cerca de la bahía</option>
                                <option value="<1H OCEAN" {% if datos.ocean_proximity == "<1H OCEAN" %}selected{% endif %}>A menos de 1 hora del océano</option>
                                <option value="INLAND" {% if datos.ocean_proximity == "INLAND" %}selected{% endif %}>Zona interior</option>
                                <option value="NEAR OCEAN" {% if datos.ocean_proximity == "NEAR OCEAN" %}selected{% endif %}>Cerca del océano</option>
                                <option value="ISLAND" {% if datos.ocean_proximity == "ISLAND" %}selected{% endif %}>Isla</option>
                            </select>
                        </div>

                    </div>

                    <button class="boton" type="submit">Estimar valor de vivienda</button>
                </form>

                <div class="nota">
                    Los valores mostrados como ejemplo corresponden a un registro del dataset. Puedes modificarlos para observar cómo cambia la predicción del modelo.
                </div>
            </div>

            <div class="resultado">
                <span class="badge">Resultado del modelo</span>
                <h2>Valor estimado</h2>

                {% if prediccion %}
                    <div class="precio">${{ "{:,.2f}".format(prediccion) }}</div>
                {% else %}
                    <div class="precio">$0.00</div>
                {% endif %}

                <p class="texto-resultado">
                    Esta cantidad representa la estimación del valor medio de las viviendas según las características ingresadas.
                </p>

               
            </div>
        </div>
    </div>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def inicio():
    prediccion = None

    datos = {
        "longitude": -122.23,
        "latitude": 37.88,
        "housing_median_age": 41,
        "total_rooms": 880,
        "total_bedrooms": 129,
        "population": 322,
        "households": 126,
        "median_income": 8.3252,
        "ocean_proximity": "NEAR BAY"
    }

    if request.method == "POST":
        datos = {
            "longitude": float(request.form["longitude"]),
            "latitude": float(request.form["latitude"]),
            "housing_median_age": float(request.form["housing_median_age"]),
            "total_rooms": float(request.form["total_rooms"]),
            "total_bedrooms": float(request.form["total_bedrooms"]),
            "population": float(request.form["population"]),
            "households": float(request.form["households"]),
            "median_income": float(request.form["median_income"]),
            "ocean_proximity": request.form["ocean_proximity"]
        }

        entrada = pd.DataFrame([datos])
        prediccion = modelo.predict(entrada)[0]
        prediccion = round(float(prediccion), 2)

    return render_template_string(HTML, prediccion=prediccion, datos=datos)


@app.route("/predecir", methods=["POST"])
def predecir():
    try:
        datos = request.get_json()

        entrada = pd.DataFrame([{
            "longitude": datos["longitude"],
            "latitude": datos["latitude"],
            "housing_median_age": datos["housing_median_age"],
            "total_rooms": datos["total_rooms"],
            "total_bedrooms": datos["total_bedrooms"],
            "population": datos["population"],
            "households": datos["households"],
            "median_income": datos["median_income"],
            "ocean_proximity": datos["ocean_proximity"]
        }])

        prediccion = modelo.predict(entrada)[0]

        return jsonify({
            "prediccion_median_house_value": round(float(prediccion), 2)
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        })


if __name__ == "__main__":
    app.run(debug=True)