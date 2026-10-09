from flask import Flask, render_template, request
import joblib
import pandas as pd

app = Flask(__name__)

# Load trained model and scaler
model = joblib.load("best_disease_prediction_model.pkl")
scaler = joblib.load("disease_prediction_scaler.pkl")


# Exact feature order used during model training
FEATURE_NAMES = [
    "age",
    "sex",
    "cp",
    "trestbps",
    "chol",
    "fbs",
    "restecg",
    "thalach",
    "exang",
    "oldpeak",
    "slope",
    "ca",
    "thal"
]


@app.route("/", methods=["GET", "POST"])
def home():

    prediction = None
    probability = None

    if request.method == "POST":

        try:
            # Get values from website form
            age = float(request.form["age"])
            sex = float(request.form["sex"])
            cp = float(request.form["cp"])
            trestbps = float(request.form["trestbps"])
            chol = float(request.form["chol"])
            fbs = float(request.form["fbs"])
            restecg = float(request.form["restecg"])
            thalach = float(request.form["thalach"])
            exang = float(request.form["exang"])
            oldpeak = float(request.form["oldpeak"])
            slope = float(request.form["slope"])
            ca = float(request.form["ca"])
            thal = float(request.form["thal"])

            # Create DataFrame with exact feature names and order
            features = pd.DataFrame([[
                age,
                sex,
                cp,
                trestbps,
                chol,
                fbs,
                restecg,
                thalach,
                exang,
                oldpeak,
                slope,
                ca,
                thal
            ]], columns=FEATURE_NAMES)

            # Scale the input data
            scaled_features = scaler.transform(features)

            # Make prediction
            result = model.predict(scaled_features)[0]

            # Get prediction probability if available
            if hasattr(model, "predict_proba"):
                probabilities = model.predict_proba(scaled_features)[0]
                probability = round(float(max(probabilities)) * 100, 2)

            # Convert model output into readable result
            if result == 1:
                prediction = "Disease Detected"
            else:
                prediction = "No Disease Detected"

        except Exception as e:

            prediction = "Error: Please check your input values."
            probability = None

            print("Prediction Error:", e)

    return render_template(
        "index.html",
        prediction=prediction,
        probability=probability
    )


if __name__ == "__main__":
    app.run(debug=True)