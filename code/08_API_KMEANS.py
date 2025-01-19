from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from joblib import load

import numpy as np
import uvicorn

# Inisialisasi aplikasi FastAPI
app = FastAPI(
    title="API Customer Segmentation dengan K MEANS",
    description="API untuk segmentasi pelanggan menggunakan K MEANS",
    version="1.0"
)

# Load model dan transformer yang telah disimpan
try:
    label_encoder_path = "../models/preprocessing/label_encoder.pkl"
    scaler_path = "../models/preprocessing/standard_scaler.pkl"
    gmm_model_path = "../models/kmeans model/kmeans_model.pkl"

    label_encoder = load(label_encoder_path)
    scaler = load(scaler_path)
    gmm_model = load(gmm_model_path)
except FileNotFoundError as e:
    raise FileNotFoundError(f"File model tidak ditemukan: {e}")

# Schema untuk input data
class InputData(BaseModel):
    gender: str  # Gender dalam format string, misalnya "Male" atau "Female"
    age: float  # Umur dalam tahun
    annual_income: float  # Pendapatan tahunan dalam ribuan dolar
    spending_score: float  # Skor pengeluaran dalam skala 1-100

# Endpoint utama untuk prediksi
@app.post("/predict", summary="Segmentasi Pelanggan")
async def predict(data: InputData):
    try:
        # Validasi gender
        if data.gender not in label_encoder.classes_:
            raise ValueError(f"Gender {data.gender} tidak valid. Pilihan: {label_encoder.classes_}")

        # Transform gender menjadi numerik
        gender_encoded = label_encoder.transform([data.gender])[0]

        # Format input sebagai array numpy
        input_features = np.array([[data.age, data.annual_income, data.spending_score]])
        input_scaled = scaler.transform(input_features)  # Skalakan data
        input_final = np.append(input_scaled[0], gender_encoded).reshape(1, -1)  # Tambahkan gender

        # Prediksi segmen menggunakan GMM
        cluster_label = gmm_model.predict(input_final)[0]

        # Hasil prediksi dengan informasi input
        return {
            "input": {
                "gender": data.gender,
                "age": data.age,
                "annual_income": data.annual_income,
                "spending_score": data.spending_score
            },
            "prediction": {
                "cluster": int(cluster_label),
                "message": f"Customer belongs to cluster {int(cluster_label)}"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Menjalankan aplikasi FastAPI dengan Uvicorn
if __name__ == "__main__":
    uvicorn.run("08_API_KMEANS:app", host="127.0.0.1", port=8000, log_level="info")