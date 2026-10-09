from flask import Flask, render_template, request
import joblib
import pandas as pd

app = Flask(__name__)

# Load trained model
model = joblib.load("random_forest_model.pkl")

# Exact feature order used by the trained model
FEATURE_NAMES = [
    'duration',
    'credit_amount',
    'installment_commitment',
    'residence_since',
    'age',
    'existing_credits',
    'num_dependents',
    'checking_status_<0',
    'checking_status_>=200',
    'checking_status_no checking',
    'credit_history_critical/other existing credit',
    'credit_history_delayed previously',
    'credit_history_existing paid',
    'credit_history_no credits/all paid',
    'purpose_new car',
    'purpose_used car',
    'purpose_business',
    'purpose_education',
    'purpose_furniture/equipment',
    'purpose_other',
    'purpose_radio/tv',
    'purpose_repairs',
    'purpose_retraining',
    'savings_status_500<=X<1000',
    'savings_status_<100',
    'savings_status_>=1000',
    'savings_status_no known savings',
    'employment_4<=X<7',
    'employment_<1',
    'employment_>=7',
    'employment_unemployed',
    'personal_status_male div/sep',
    'personal_status_male mar/wid',
    'personal_status_male single',
    'other_parties_guarantor',
    'other_parties_none',
    'property_magnitude_no known property',
    'property_magnitude_real estate',
    'property_magnitude_car',
    'other_payment_plans_none',
    'other_payment_plans_stores',
    'housing_own',
    'housing_rent',
    'job_unemp/unskilled non res',
    'job_unskilled resident',
    'job_skilled',
    'own_telephone_yes',
    'foreign_worker_yes'
]


@app.route("/", methods=["GET", "POST"])
def home():

    prediction = None
    confidence = None
    error = None

    if request.method == "POST":

        try:
            # -------------------------------------------------
            # Get numerical inputs
            # -------------------------------------------------

            duration = float(request.form["duration"])
            credit_amount = float(request.form["credit_amount"])
            installment_commitment = float(
                request.form["installment_commitment"]
            )
            residence_since = float(request.form["residence_since"])
            age = float(request.form["age"])
            existing_credits = float(request.form["existing_credits"])
            num_dependents = float(request.form["num_dependents"])

            # -------------------------------------------------
            # Basic backend validation
            # -------------------------------------------------

            if duration <= 0:
                raise ValueError("Invalid loan duration.")

            if credit_amount <= 0:
                raise ValueError("Invalid credit amount.")

            if installment_commitment < 1 or installment_commitment > 4:
                raise ValueError("Invalid installment commitment.")

            if residence_since < 1 or residence_since > 4:
                raise ValueError("Invalid residence value.")

            if age < 18 or age > 100:
                raise ValueError("Invalid age.")

            if existing_credits < 1:
                raise ValueError("Invalid existing credits.")

            if num_dependents < 1:
                raise ValueError("Invalid number of dependents.")

            # -------------------------------------------------
            # Create all 48 features with value 0
            # -------------------------------------------------

            features = {feature: 0 for feature in FEATURE_NAMES}

            # Numerical features
            features["duration"] = duration
            features["credit_amount"] = credit_amount
            features["installment_commitment"] = installment_commitment
            features["residence_since"] = residence_since
            features["age"] = age
            features["existing_credits"] = existing_credits
            features["num_dependents"] = num_dependents

            # -------------------------------------------------
            # Checking Status
            # -------------------------------------------------

            checking_status = request.form["checking_status"]

            if checking_status == "less_0":
                features["checking_status_<0"] = 1

            elif checking_status == "200_plus":
                features["checking_status_>=200"] = 1

            elif checking_status == "no_checking":
                features["checking_status_no checking"] = 1

            # -------------------------------------------------
            # Credit History
            # -------------------------------------------------

            credit_history = request.form["credit_history"]

            if credit_history == "critical":
                features[
                    "credit_history_critical/other existing credit"
                ] = 1

            elif credit_history == "delayed":
                features["credit_history_delayed previously"] = 1

            elif credit_history == "existing_paid":
                features["credit_history_existing paid"] = 1

            elif credit_history == "no_credits":
                features[
                    "credit_history_no credits/all paid"
                ] = 1

            # -------------------------------------------------
            # Purpose
            # -------------------------------------------------

            purpose = request.form["purpose"]

            purpose_mapping = {
                "new_car": "purpose_new car",
                "used_car": "purpose_used car",
                "business": "purpose_business",
                "education": "purpose_education",
                "furniture": "purpose_furniture/equipment",
                "other": "purpose_other",
                "radio_tv": "purpose_radio/tv",
                "repairs": "purpose_repairs",
                "retraining": "purpose_retraining"
            }

            if purpose in purpose_mapping:
                features[purpose_mapping[purpose]] = 1

            # -------------------------------------------------
            # Savings Status
            # -------------------------------------------------

            savings_status = request.form["savings_status"]

            savings_mapping = {
                "500_1000": "savings_status_500<=X<1000",
                "less_100": "savings_status_<100",
                "1000_plus": "savings_status_>=1000",
                "no_savings": "savings_status_no known savings"
            }

            if savings_status in savings_mapping:
                features[savings_mapping[savings_status]] = 1

            # -------------------------------------------------
            # Employment
            # -------------------------------------------------

            employment = request.form["employment"]

            employment_mapping = {
                "4_7": "employment_4<=X<7",
                "less_1": "employment_<1",
                "7_plus": "employment_>=7",
                "unemployed": "employment_unemployed"
            }

            if employment in employment_mapping:
                features[employment_mapping[employment]] = 1

            # -------------------------------------------------
            # Personal Status
            # -------------------------------------------------

            personal_status = request.form["personal_status"]

            personal_mapping = {
                "male_div_sep": "personal_status_male div/sep",
                "male_mar_wid": "personal_status_male mar/wid",
                "male_single": "personal_status_male single"
            }

            if personal_status in personal_mapping:
                features[personal_mapping[personal_status]] = 1

            # -------------------------------------------------
            # Other Parties
            # -------------------------------------------------

            other_parties = request.form["other_parties"]

            if other_parties == "guarantor":
                features["other_parties_guarantor"] = 1

            elif other_parties == "none":
                features["other_parties_none"] = 1

            # -------------------------------------------------
            # Property
            # -------------------------------------------------

            property_magnitude = request.form["property_magnitude"]

            property_mapping = {
                "no_property": "property_magnitude_no known property",
                "real_estate": "property_magnitude_real estate",
                "car": "property_magnitude_car"
            }

            if property_magnitude in property_mapping:
                features[property_mapping[property_magnitude]] = 1

            # -------------------------------------------------
            # Other Payment Plans
            # -------------------------------------------------

            payment_plan = request.form["other_payment_plans"]

            if payment_plan == "none":
                features["other_payment_plans_none"] = 1

            elif payment_plan == "stores":
                features["other_payment_plans_stores"] = 1

            # -------------------------------------------------
            # Housing
            # -------------------------------------------------

            housing = request.form["housing"]

            if housing == "own":
                features["housing_own"] = 1

            elif housing == "rent":
                features["housing_rent"] = 1

            # -------------------------------------------------
            # Job
            # -------------------------------------------------

            job = request.form["job"]

            job_mapping = {
                "unemp_non_res": "job_unemp/unskilled non res",
                "unskilled": "job_unskilled resident",
                "skilled": "job_skilled"
            }

            if job in job_mapping:
                features[job_mapping[job]] = 1

            # -------------------------------------------------
            # Telephone
            # -------------------------------------------------

            telephone = request.form["own_telephone"]

            if telephone == "yes":
                features["own_telephone_yes"] = 1

            # -------------------------------------------------
            # Foreign Worker
            # -------------------------------------------------

            foreign_worker = request.form["foreign_worker"]

            if foreign_worker == "yes":
                features["foreign_worker_yes"] = 1

            # -------------------------------------------------
            # Create DataFrame in exact model feature order
            # -------------------------------------------------

            input_data = pd.DataFrame(
                [[features[name] for name in FEATURE_NAMES]],
                columns=FEATURE_NAMES
            )

            # -------------------------------------------------
            # Prediction
            # -------------------------------------------------

            result = model.predict(input_data)[0]

            # Class label
            if result == 1:
                prediction = "Good Credit Risk"
            else:
                prediction = "Poor Credit Risk"

            # -------------------------------------------------
            # Model Confidence
            # -------------------------------------------------

            if hasattr(model, "predict_proba"):
                probabilities = model.predict_proba(input_data)[0]
                confidence = round(max(probabilities) * 100, 2)

        except Exception as e:

            print("Prediction Error:", e)

            error = (
                "Unable to process the prediction. "
                "Please check your input values and try again."
            )

    return render_template(
        "index.html",
        prediction=prediction,
        confidence=confidence,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)