# Import library yang dibutuhkan
import streamlit as st  # Library untuk membuat aplikasi berbasis web
import numpy as np  # Library untuk komputasi numerik
import pandas as pd  # Library untuk pengolahan data frame dan file

import matplotlib.pyplot as plt  # Library untuk membuat visualisasi data
import seaborn as sns  # Library untuk membuat visualisasi data yang lebih menarik
import warnings  # Library untuk menangani peringatan selama komputasi

from sklearn.preprocessing import StandardScaler, LabelEncoder  # Library untuk preprocessing dan normalisasi data
from sklearn.decomposition import PCA  # Library untuk ekstraksi fitur utama
from fcmeans import FCM  # Library untuk membuat model fuzzy c-means

# Set konfigurasi halaman Streamlit
st.set_page_config(
    page_title="Customer Segmentation with FCM",  # Judul aplikasi
    layout="wide",  # Tata letak aplikasi
    initial_sidebar_state="expanded"  # Posisi awal sidebar
)

# Fungsi untuk memuat data dari file CSV
@st.cache_data
def load_data():
    # Load dataset dari file CSV
    df = pd.read_csv('../data/Mall_Customers.csv')
    return df

# Fungsi untuk melakukan preprocessing data
@st.cache_data
def preprocess_data(df):
    # Normalisasi kolom "Annual Income (k$)" untuk menghilangkan outlier
    df['Annual Income (k$)'] = np.clip(
        df['Annual Income (k$)'],
        df['Annual Income (k$)'].quantile(0.05),  # Ambil kuantil ke-5 sebagai batas bawah
        df['Annual Income (k$)'].quantile(0.95)  # Ambil kuantil ke-95 sebagai batas atas
    )

    # Normalisasi kolom "Spending Score (1-100)" untuk menghilangkan outlier
    df['Spending Score (1-100)'] = np.clip(
        df['Spending Score (1-100)'],
        df['Spending Score (1-100)'].quantile(0.05),
        df['Spending Score (1-100)'].quantile(0.95)
    )

    # Ubah data kategorik pada kolom "Gender" menjadi numerik dengan LabelEncoder
    label_encoder = LabelEncoder()
    df['Gender'] = label_encoder.fit_transform(df['Gender'])

    # Lakukan normalisasi data pada fitur "Age", "Annual Income", dan "Spending Score"
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(df[['Age', 'Annual Income (k$)', 'Spending Score (1-100)']])
    return scaled_data, df, scaler

# Fungsi untuk melatih model Fuzzy C-Means (FCM)
@st.cache_resource
def train_fcm(data, n_clusters):
    # Buat model Fuzzy C-Means dengan jumlah klaster tertentu
    fcm = FCM(n_clusters=n_clusters, random_state=42)
    # Prediksi klaster menggunakan data yang telah dinormalisasi
    fcm.fit(data)
    fcm_labels = fcm.predict(data)
    return fcm, fcm_labels

# Assign cluster name
def assign_cluster_names(cluster_id):
    cluster_names = {
        0: "Budget-Conscious",
        1: "Middle-Class",
        2: "Aspiring-Spenders",
        3: "Affluent Elites"
    }
    return cluster_names.get(cluster_id, "Unknown Cluster")

# Fungsi untuk membuat prediksi klaster berdasarkan input pengguna
def predict_cluster(age, income, spending, model, scaler):
    # Buat array fitur berdasarkan input pengguna
    features = np.array([[age, income, spending]])
    # Normalisasi data input menggunakan scaler yang sudah dilatih
    scaled_features = scaler.transform(features)
    # Prediksi klaster berdasarkan data yang diinputkan
    cluster = model.predict(scaled_features)[0]
    return cluster

# Fungsi untuk visualisasi klaster menggunakan PCA (Principal Component Analysis)
def plot_clusters(data, labels):
    # Lakukan PCA untuk mereduksi dimensi data menjadi 2 dimensi
    pca = PCA(n_components=2)
    data_pca = pca.fit_transform(data)
    plt.figure(figsize=(10, 6))  # Atur ukuran plot
    plt.scatter(data_pca[:, 0], data_pca[:, 1], c=labels, cmap='viridis', s=50)  # Buat scatter plot
    plt.title('Customer Segmentation with FCM')  # Judul plot
    plt.xlabel('Principal Component 1')  # Label sumbu X
    plt.ylabel('Principal Component 2')  # Label sumbu Y
    plt.colorbar(label='Cluster')  # Tambahkan colorbar
    st.pyplot(plt)  # Tampilkan plot di Streamlit

# Fungsi utama untuk aplikasi Streamlit
def main():
    # Judul aplikasi
    st.title("Customer Segmentation with Fuzzy C-Means")

    # Sidebar untuk pengaturan jumlah klaster
    st.sidebar.header("Options")
    n_clusters = st.sidebar.slider("Select Number of Clusters", min_value=2, max_value=10, value=4)  # Slider untuk memilih jumlah klaster

    # Load data dan lakukan preprocessing
    df = load_data()
    scaled_data, df_preprocessed, scaler = preprocess_data(df)

    # Latih model FCM dengan jumlah klaster yang dipilih
    fcm, fcm_labels = train_fcm(scaled_data, n_clusters)
    df_preprocessed['Cluster'] = fcm_labels  # Tambahkan label klaster ke data

    # Tampilkan data dan ringkasan klaster
    st.subheader("Dataset Preview")
    st.write(df.head())  # Tampilkan beberapa baris pertama dataset

    st.subheader(f"Cluster Distribution (n_clusters={n_clusters})")
    cluster_counts = df_preprocessed['Cluster'].value_counts().sort_index()  # Hitung distribusi klaster
    st.bar_chart(cluster_counts)  # Tampilkan distribusi klaster sebagai bar chart

    # Visualisasi klaster
    st.subheader("Cluster Visualization")
    plot_clusters(scaled_data, fcm_labels)  # Panggil fungsi visualisasi

    # Tampilkan ringkasan statistik untuk setiap klaster
    st.subheader("Cluster Summaries")
    cluster_summary = df_preprocessed.groupby('Cluster')[['Age', 'Annual Income (k$)', 'Spending Score (1-100)']].mean()
    st.dataframe(cluster_summary)  # Tampilkan ringkasan sebagai tabel

    # Sidebar untuk input pengguna untuk prediksi
    st.sidebar.subheader("Predict Cluster")
    age_input = st.sidebar.number_input("Age", min_value=0, max_value=100, value=30)  # Input usia
    income_input = st.sidebar.number_input("Annual Income (k$)", min_value=0, max_value=200, value=50)  # Input pendapatan tahunan
    spending_input = st.sidebar.number_input("Spending Score (1-100)", min_value=0, max_value=100, value=50)  # Input skor pengeluaran

    # Tombol untuk melakukan prediksi
    if st.sidebar.button("Predict"):
        predicted_cluster = predict_cluster(age_input, income_input, spending_input, fcm, scaler)  # Lakukan prediksi
        cluster_name = assign_cluster_names(predicted_cluster)  # Ambil nama klaster berdasarkan hasil prediksi
        st.sidebar.success(f"The predicted cluster is: {cluster_name} ({predicted_cluster})")  # Tampilkan hasil prediksi

# Jalankan aplikasi jika file ini dieksekusi sebagai program utama
if __name__ == "__main__":
    main()
