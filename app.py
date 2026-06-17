from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Cargar modelo entrenado
modelo = joblib.load("modelo_regresion_california.pkl")

@app.route("/")
def inicio():
    return "Modelo de regresión California Housing funcionando correctamente."

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