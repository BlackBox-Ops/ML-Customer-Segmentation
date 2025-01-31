import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

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
    df = pd.read_csv('../data/Mall_Customers.csv')
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

# Assign cluster names
def assign_cluster_names(cluster_id):
    cluster_names = {
        0: "Budget-Conscious",
        1: "Balenced-Spenders",
        2: "High-Spenders",
        3: "Wealthy Elites"
    }
    return cluster_names.get(cluster_id, "Unknown Cluster")

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

# Visualize stacked bar chart
def plot_stacked_bar(df):
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    # Plot untuk rata-rata pendapatan tahunan
    sns.barplot(
        x='kategori_usia',
        y='Annual Income (k$)',
        hue='Cluster',
        data=df,
        ax=axes[0],
        palette='viridis'
    )
    axes[0].set_title("Rata-rata Pendapatan Tahunan Berdasarkan Kategori Usia dan Klaster")
    axes[0].set_xlabel("Kategori Usia")
    axes[0].set_ylabel("Pendapatan Tahunan")

    # Plot untuk skor pengeluaran
    sns.barplot(
        x='kategori_usia',
        y='Spending Score (1-100)',
        hue='Cluster',
        data=df,
        ax=axes[1],
        palette='viridis'
    )
    axes[1].set_title("Skor Pengeluaran Berdasarkan Kategori Usia dan Klaster")
    axes[1].set_xlabel("Kategori Usia")
    axes[1].set_ylabel("Skor Pengeluaran")

    st.pyplot(fig)

# Main function
def main():
    st.title("Customer Segmentation with GMM")
    st.sidebar.header("Options")
    n_clusters = st.sidebar.slider("Select Number of Clusters", min_value=2, max_value=10, value=4)
    
    # Load and preprocess data
    df = load_data()
    scaled_data, df_preprocessed, scaler = preprocess_data(df)
    
    # Add age categories
    bins = [0, 25, 40, 60, 100]
    labels = ['Young Adult', 'Adult', 'Middle Age', 'Senior']
    df_preprocessed['kategori_usia'] = pd.cut(df_preprocessed['Age'], bins=bins, labels=labels)

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

    # Stacked bar chart
    st.subheader("Cluster Analysis by Age Category")
    plot_stacked_bar(df_preprocessed)

    # Input pengguna untuk prediksi
    st.sidebar.subheader("Predict Cluster")
    age_input = st.sidebar.number_input("Age", min_value=0, max_value=100, value=30)
    income_input = st.sidebar.number_input("Annual Income (k$)", min_value=0, max_value=200, value=50)
    spending_input = st.sidebar.number_input("Spending Score (1-100)", min_value=0, max_value=100, value=50)

    # Tombol untuk melakukan prediksi
    if st.sidebar.button("Predict"):
        predicted_cluster = predict_cluster(age_input, income_input, spending_input, gmm, scaler)
        cluster_name = assign_cluster_names(predicted_cluster)
        st.sidebar.success(f"The predicted cluster is: {cluster_name} (Cluster ID: {predicted_cluster})")

# Run the app
if __name__ == "__main__":
    main()
