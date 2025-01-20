# Import library yang dibutuhkan
import streamlit as st  # Library untuk membuat aplikasi berbasis web
import numpy as np  # Library untuk komputasi numerik
import pandas as pd  # Library untuk pengolahan DataFrame dan file

import matplotlib.pyplot as plt  # Library untuk membuat visualisasi data
import seaborn as sns  # Library untuk membuat visualisasi data yang menarik
from sklearn.preprocessing import StandardScaler, LabelEncoder  # Library untuk preprocessing dan normalisasi data
from sklearn.decomposition import PCA  # Library untuk ekstraksi fitur utama
from sklearn.cluster import KMeans  # Library untuk model K-Means

# Set konfigurasi halaman Streamlit
st.set_page_config(
    page_title="Customer Segmentation with K-Means",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Fungsi untuk memuat data dari file CSV
@st.cache_data
def load_data():
    df = pd.read_csv('../data/Mall_Customers.csv')
    return df

# Fungsi untuk melakukan preprocessing data
@st.cache_data
def preprocess_data(df):
    # Normalisasi kolom "Annual Income (k$)" untuk menghilangkan outlier
    df['Annual Income (k$)'] = np.clip(
        df['Annual Income (k$)'],
        df['Annual Income (k$)'].quantile(0.05),
        df['Annual Income (k$)'].quantile(0.95)
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

# Fungsi untuk melatih model K-Means
@st.cache_resource
def train_kmeans(data, n_clusters):
    kmeans = KMeans(n_clusters=n_clusters, random_state=42).fit(data)
    kmeans_labels = kmeans.predict(data)
    return kmeans, kmeans_labels

# Fungsi untuk memberikan nama pada klaster
def assign_cluster_names(cluster_id):
    cluster_names = {
        0: "Konsumen Rendah",
        1: "Konsumen Sedang",
        2: "Konsumen Stabil",
        3: "Konsumen Mapan"
    }
    return cluster_names.get(cluster_id, "Unknown Cluster")

# Fungsi untuk membuat prediksi klaster berdasarkan input pengguna
def predict_cluster(age, income, spending, model, scaler):
    features = np.array([[age, income, spending]])
    scaled_features = scaler.transform(features)
    cluster = model.predict(scaled_features)[0]
    return cluster

# Fungsi untuk visualisasi klaster menggunakan PCA
def plot_clusters(data, labels):
    pca = PCA(n_components=2)
    data_pca = pca.fit_transform(data)
    plt.figure(figsize=(10, 6))
    plt.scatter(data_pca[:, 0], data_pca[:, 1], c=labels, cmap='viridis', s=50)
    plt.title('Customer Segmentation with K-Means')
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.colorbar(label='Cluster')
    st.pyplot(plt)

# Fungsi utama untuk aplikasi Streamlit
def main():
    st.title("Customer Segmentation with K-Means")

    # Sidebar untuk pengaturan jumlah klaster
    st.sidebar.header("Options")
    n_clusters = st.sidebar.slider("Select Number of Clusters", min_value=2, max_value=10, value=4)

    # Load data dan lakukan preprocessing
    df = load_data()
    scaled_data, df_preprocessed, scaler = preprocess_data(df)

    # Latih model K-Means dengan jumlah klaster yang dipilih
    kmeans, kmeans_labels = train_kmeans(scaled_data, n_clusters)
    df_preprocessed['Cluster'] = kmeans_labels

    # Tampilkan data dan ringkasan klaster
    st.subheader("Dataset Preview")
    st.write(df.head())

    st.subheader(f"Cluster Distribution (n_clusters={n_clusters})")
    cluster_counts = df_preprocessed['Cluster'].value_counts().sort_index()
    st.bar_chart(cluster_counts)

    # Visualisasi klaster
    st.subheader("Cluster Visualization")
    plot_clusters(scaled_data, kmeans_labels)

    # Tampilkan ringkasan statistik untuk setiap klaster
    st.subheader("Cluster Summaries")
    cluster_summary = df_preprocessed.groupby('Cluster')[['Age', 'Annual Income (k$)', 'Spending Score (1-100)']].mean()
    st.dataframe(cluster_summary)

    # Sidebar untuk input pengguna untuk prediksi
    st.sidebar.subheader("Predict Cluster")
    age_input = st.sidebar.number_input("Age", min_value=0, max_value=100, value=30)
    income_input = st.sidebar.number_input("Annual Income (k$)", min_value=0, max_value=200, value=50)
    spending_input = st.sidebar.number_input("Spending Score (1-100)", min_value=0, max_value=100, value=50)

    # Tombol untuk melakukan prediksi
    if st.sidebar.button("Predict"):
        predicted_cluster = predict_cluster(age_input, income_input, spending_input, kmeans, scaler)
        cluster_name = assign_cluster_names(predicted_cluster)
        st.sidebar.success(f"The predicted cluster is: {cluster_name} ({predicted_cluster})")

# Jalankan aplikasi jika file ini dieksekusi sebagai program utama
if __name__ == "__main__":
    main()
