import joblib

# Load model
model = joblib.load("random_forest_model.pkl")

print("=" * 50)
print("SMART CREDIT SCORING MODEL")
print("=" * 50)

print("\nModel Type:")
print(type(model))

print("\nNumber of Features:")
print(model.n_features_in_)

print("\nFeature Names:")

if hasattr(model, "feature_names_in_"):
    print(model.feature_names_in_)
else:
    print("Feature names were not stored in the model.")

print("\nClasses:")
print(model.classes_)

print("\nModel Loaded Successfully!")