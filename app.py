import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.decomposition import PCA

# Set page configuration
st.set_page_config(
    page_title="Customer Segmentation",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('./data/Mall_Customers.csv')
    return df

# Preprocessing function
@st.cache_data
def preprocess_data(df):
    # Winsorize annual income and spending score
    df['Annual Income (k$)'] = np.clip(
        df['Annual Income (k$)'],
        df['Annual Income (k$)'].quantile(0.05),
        df['Annual Income (k$)'].quantile(0.95)
    )
    
    df['Spending Score (1-100)'] = np.clip(
        df['Spending Score (1-100)'],
        df['Spending Score (1-100)'].quantile(0.05),
        df['Spending Score (1-100)'].quantile(0.95)
    )
    # Encode Gender
    label_encoder = LabelEncoder()
    df['Gender'] = label_encoder.fit_transform(df['Gender'])
    # Standardize data
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(df[['Age', 'Annual Income (k$)', 'Spending Score (1-100)']])
    return scaled_data, df, scaler

# Train GMM model
@st.cache_resource
def train_gmm(data, n_clusters):
    gmm = GaussianMixture(n_components=n_clusters, random_state=42)
    gmm_labels = gmm.fit_predict(data)
    return gmm, gmm_labels

# Predict cluster
def predict_cluster(age, income, spending, model, scaler):
    # Buat array fitur
    features = np.array([[age, income, spending]])
    # Standarisasi data input
    scaled_features = scaler.transform(features)
    # Prediksi klaster
    cluster = model.predict(scaled_features)[0]
    return cluster

# Visualize clusters with PCA
def plot_clusters(data, labels):
    pca = PCA(n_components=2)
    data_pca = pca.fit_transform(data)
    plt.figure(figsize=(10, 6))
    plt.scatter(data_pca[:, 0], data_pca[:, 1], c=labels, cmap='viridis', s=50)
    plt.title('Customer Segmentation with GMM')
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.colorbar(label='Cluster')
    st.pyplot(plt)

# Main function
def main():
    st.title("Customer Segmentation with GMM")
    st.sidebar.header("Options")
    n_clusters = st.sidebar.slider("Select Number of Clusters", min_value=2, max_value=10, value=4)
    
    # Load and preprocess data
    df = load_data()
    scaled_data, df_preprocessed, scaler = preprocess_data(df)
    
    # Train GMM model
    gmm, gmm_labels = train_gmm(scaled_data, n_clusters)
    df_preprocessed['Cluster'] = gmm_labels
    
    # Display data and summary
    st.subheader("Dataset Preview")
    st.write(df.head())
    
    st.subheader(f"Cluster Distribution (n_clusters={n_clusters})")
    cluster_counts = df_preprocessed['Cluster'].value_counts().sort_index()
    st.bar_chart(cluster_counts)
    
    # Visualize clusters
    st.subheader("Cluster Visualization")
    plot_clusters(scaled_data, gmm_labels)
    
    # Show cluster summaries
    st.subheader("Cluster Summaries")
    cluster_summary = df_preprocessed.groupby('Cluster')[['Age', 'Annual Income (k$)', 'Spending Score (1-100)']].mean()
    st.dataframe(cluster_summary)

    # Input pengguna untuk prediksi
    st.sidebar.subheader("Predict Cluster")
    age_input = st.sidebar.number_input("Age", min_value=0, max_value=100, value=30)
    income_input = st.sidebar.number_input("Annual Income (k$)", min_value=0, max_value=200, value=50)
    spending_input = st.sidebar.number_input("Spending Score (1-100)", min_value=0, max_value=100, value=50)

    # Tombol untuk melakukan prediksi
    if st.sidebar.button("Predict"):
        predicted_cluster = predict_cluster(age_input, income_input, spending_input, gmm, scaler)
        st.sidebar.success(f"The predicted cluster is: {predicted_cluster}")

# Run the app
if __name__ == "__main__":
    main()
