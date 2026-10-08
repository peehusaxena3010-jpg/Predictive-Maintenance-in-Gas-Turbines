# Example helper to save models dict to models/rf_models.pkl
# Run this from the environment where `rf_models` exists, or modify to load the models first.
import os
import joblib

# Suppose rf_models is a dict containing the trained RandomForestRegressor objects.
# If you trained the models in a notebook, run:
# joblib.dump(rf_models, "models/rf_models.pkl")
#
# This file is only an example. Replace rf_models below with your actual trained dict.

if __name__ == "__main__":
    # Example placeholder: do NOT run unless you set rf_models variable.
    # rf_models = {...}  # create or import from your training script
    # os.makedirs("models", exist_ok=True)
    # joblib.dump(rf_models, "models/rf_models.pkl")
    print("This file demonstrates where/how to joblib.dump your rf_models dict.")
    print("From your notebook run: joblib.dump(rf_models, 'models/rf_models.pkl')")
