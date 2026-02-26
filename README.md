# 🌿 GreenMind AI – Smart Energy Optimization System

> An AI-powered energy usage prediction system built with **RandomForest**, **FastAPI**, and **Streamlit**.

---

## 📁 Project Structure

```
greenmind-ai/
├── data/
│   └── energy_data.csv          # Training dataset
├── models/
│   ├── train.py                  # ML training script
│   └── energy_model.pkl          # Saved model (generated)
├── api/
│   └── main.py                   # FastAPI backend
├── app/
│   └── dashboard.py              # Streamlit UI
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🚀 Quick Start (Local)

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/greenmind-ai.git
cd greenmind-ai
```

### 2. Create and activate a virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Train the model

```bash
python models/train.py
```

This generates `models/energy_model.pkl` and prints the R² accuracy score.

### 5. Start the FastAPI backend

```bash
uvicorn api.main:app --reload --port 8000
```

- API root: [http://localhost:8000](http://localhost:8000)
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

### 6. Launch the Streamlit dashboard

In a **new terminal** (with venv activated):

```bash
streamlit run app/dashboard.py
```

- Dashboard: [http://localhost:8501](http://localhost:8501)

---

## 🔌 API Endpoints

| Method | Endpoint   | Description                  |
|--------|------------|------------------------------|
| GET    | `/`        | Health check                 |
| POST   | `/predict` | Energy usage prediction (kWh)|
| GET    | `/docs`    | Swagger UI                   |

### POST `/predict` – Example

**Request:**
```json
{
  "temperature": 32.5,
  "humidity": 60,
  "hour": 14
}
```

**Response:**
```json
{
  "predicted_energy": 6.823,
  "unit": "kWh"
}
```

**Validation rules:**
- `temperature`: 0 – 60°C
- `humidity`: 0 – 100%
- `hour`: 0 – 23

---

