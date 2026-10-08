# Predictive Maintenance in Gas Turbines (AI Bearing Analyzer)

An AI-driven predictive maintenance system for industrial gas turbines. The application uses Machine Learning (Random Forest regression) to monitor bearing health, estimate turbine speed, and predict bearing metal temperatures from operational vibration and load data.

---

## 🚀 Features

- **Multi-Bearing Analysis**: Analyzes sensor readings across 5 turbine bearings.
- **Speed & Temperature Prediction**: Uses trained `RandomForestRegressor` models to estimate operational speed and bearing metal temperatures.
- **Health Condition Status**:
  - **Normal**: Temperature < 80°C
  - **Warning**: Temperature between 80°C and 91°C
  - **Critical**: Temperature $\ge$ 91°C
- **Interactive Web Interface**: Clean web dashboard built with TailwindCSS and Chart.js for visualization of temperature, vibration, and bearing health status.

---

## 🛠️ Tech Stack

- **Backend**: Python, Flask, Flask-CORS
- **Machine Learning & Data**: scikit-learn, pandas, numpy, openpyxl, joblib
- **Frontend**: HTML5, TailwindCSS, Chart.js

---

## 📂 Project Structure

```text
├── data/
│   ├── training_data.xlsx       # Operational sensor dataset for model training
│   └── testing_data.xlsx        # Test dataset
├── models/
│   └── rf_models.pkl            # Serialized trained model weights
├── static/
│   ├── css/
│   │   └── styles.css           # Custom UI styling
│   └── js/
│       └── main.js              # Frontend logic and Chart.js integration
├── templates/
│   └── index.html               # Main dashboard UI
├── app.py                       # Flask server and prediction API
├── save_models.py               # Model export utility script
├── requirements.txt             # Python dependencies
└── README.md
```

---

## ⚡ Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/peehusaxena3010-jpg/Predictive-Maintenance-in-Gas-Turbines.git
cd Predictive-Maintenance-in-Gas-Turbines
```

### 2. Set Up a Virtual Environment

```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python app.py
```

Open your browser and navigate to `http://localhost:5000` to interact with the dashboard.
