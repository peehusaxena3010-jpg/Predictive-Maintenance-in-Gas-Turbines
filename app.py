from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import warnings
warnings.filterwarnings("ignore", message="X does not have valid feature names", category=UserWarning)


app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

def load_and_clean_data():
    train_file = "data/training_data.xlsx"
    test_file = "data/testing_data.xlsx"

    # Read Excel files
    train_df = pd.read_excel(train_file, header=1, skiprows=[2, 3, 4])
    test_df = pd.read_excel(test_file, header=1, skiprows=[2, 3, 4])

    # Safe datetime conversion (no dtype warning)
    train_dates = pd.to_datetime(train_df.iloc[:, 0].astype(str), errors="coerce")
    test_dates = pd.to_datetime(test_df.iloc[:, 0].astype(str), errors="coerce")

    # Drop old column and insert clean Timestamp column
    first_col_name = train_df.columns[0]
    train_df = train_df.drop(columns=[first_col_name])
    train_df.insert(0, "Timestamp", train_dates)

    first_col_name = test_df.columns[0]
    test_df = test_df.drop(columns=[first_col_name])
    test_df.insert(0, "Timestamp", test_dates)

    # Data cleaning logic
    def clean_data(df):
        df = df.copy()
        for col in df.columns[1:]:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        if "Load" in df.columns:
            df = df[df["Load"] >= 0]
        if "Speed" in df.columns:
            df = df[df["Speed"] > 0]

        vib_cols = [c for c in df.columns if "Vibration" in c]
        for c in vib_cols:
            df = df[df[c] <= 50]

        temp_cols = [c for c in df.columns if "Metal" in c]
        for c in temp_cols:
            df = df[df[c] <= 200]

        df.fillna(df.mean(numeric_only=True), inplace=True)
        return df

    return clean_data(train_df)


def train_models():
    print("Training models...")
    train_clean = load_and_clean_data()
    rf_models = {}

    # Model to predict Speed
    X_train = train_clean[
        [
            "Load",
            "Bearing 1 Vibration",
            "Bearing 2 Vibration",
            "Bearing 3 Vibration",
            "Bearing 4 Vibration",
            "Bearing 5 Vibration",
        ]
    ]
    y_train = train_clean["Speed"]
    rf_speed = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_speed.fit(X_train, y_train)
    rf_models["Speed"] = rf_speed

    # Models to predict Metal Temperatures
    for i in range(1, 6):
        vib = f"Bearing {i} Vibration"
        temp = f"Bearing {i} Metal temperature"
        X_train = train_clean[["Load", "Speed", vib]]
        y_train = train_clean[temp]
        rf = RandomForestRegressor(n_estimators=100, random_state=42)
        rf.fit(X_train, y_train)
        rf_models[temp] = rf

    print("Models trained successfully.")
    return rf_models


# Train once at startup
rf_models = train_models()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    load = float(data["load"])
    vibrations = [float(v) for v in data["vibrations"]]

    # Predict Speed
    X_speed = np.array([[load] + vibrations])
    speed_pred = rf_models["Speed"].predict(X_speed)[0]

    # Predict each bearing's metal temperature
    results = []
    for i in range(1, 6):
        vib = vibrations[i - 1]
        X_temp = np.array([[load, speed_pred, vib]])
        temp_pred = rf_models[f"Bearing {i} Metal temperature"].predict(X_temp)[0]

        # Determine condition
        if temp_pred >= 91:
            status = "Critical"
        elif temp_pred >= 80:
            status = "Warning"
        else:
            status = "Normal"

        results.append(
            {
                "bearing": i,
                "speed": round(speed_pred, 2),
                "temperature": round(temp_pred, 2),
                "status": status,
            }
        )

    return jsonify({"predictions": results})


if __name__ == "__main__":
    app.run(debug=False)
