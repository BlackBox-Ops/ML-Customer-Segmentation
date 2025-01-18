# load library yang digunakan 
import numpy as np  # pustaka untuk komputasi numerik 
import pandas as pd # pustaka untuk pengolahan dataframe 
import joblib  # pustaka untuk load model ke dalam format joblib 
import warnings  # pustaka untuk handling error pada proses komputasi 

from scipy.stats.mstats import winsorize # Library untuk handling outlier
from sklearn.preprocessing import LabelEncoder, StandardScaler # Library untuk preprocessing data numerik dan kategorik

from sklearn.mixture import GaussianMixture  # Library untuk load model GMM 
from sklearn.metrics import silhouette_score, davies_bouldin_score # Library untuk pengukuran model

# Buat variabel untuk handling error pada saat proses komputasi
warnings.filterwarnings('ignore')

# Load dataframe yang digunakan 
df = pd.read_csv('../data/Mall_Customers.csv')

# Hapus nilai outlier dari kolom annual income dan spending score menggunakan teknik winsorize 
df['Annual Income (k$)'] = winsorize(df['Annual Income (k$)'], limits=[0.05, 0.05])
df['Spending Score (1-100)'] = winsorize(df['Spending Score (1-100)'], limits=[0.05, 0.05])

# hapus kolom customer id 
df.drop(['CustomerID'], axis=1, inplace=True)

# Preprocessing kolom kategorik menjadi numerik menggunakan LabelEncoder
label_encoder = LabelEncoder()
df['Gender'] = label_encoder.fit_transform(df['Gender'])

# Pisahkan kolom gender dan hapus kolom gender dari DataFrame
Gender = df['Gender']
df.drop('Gender', axis=1, inplace=True)

# Preprocessing kolom numerik dengan z-score
scaler = StandardScaler()
scaled_data = scaler.fit_transform(df[['Age', 'Annual Income (k$)', 'Spending Score (1-100)']])

# Buat DataFrame baru dari hasil transformasi
df_customer_scaled = pd.DataFrame(scaled_data, columns=['Age', 'Annual Income (k$)', 'Spending Score (1-100)'])

# Gabungkan kolom Gender yang telah disimpan sebelumnya
df_customer_scaled['Gender'] = Gender

# buat model gmm 
gmm = GaussianMixture(n_components=4, random_state=42)
gmm.fit_predict(df_customer_scaled)
gmm_labels = gmm.predict(df_customer_scaled)

sil_score = silhouette_score(df_customer_scaled, gmm_labels)
print(f'silhouette score : {sil_score:.3f}')

# Hitung Davies-Boundin Index
db_index = davies_bouldin_score(df_customer_scaled, gmm_labels)
print(f'Davies-Boundin Index : {db_index:.3f}')

# load datasheet untuk digabungan dengan hasil k-means 
data = pd.read_csv('../data/kmeans.csv')

# simpan hasil klaster ke c-means 
data['GMM'] = gmm_labels
print(data)

# simpan file hasil transformasi ke dalam bentuk format csv 
data.to_csv('../data/GMM.csv', index=False)

# Simpan model dan scaler
joblib.dump(label_encoder, '../models/gmm model/label_encoder.pkl')
joblib.dump(scaler, '../models/gmm model/standard_scaler.pkl')
joblib.dump(gmm, '../models/gmm model/gmm_model.pkl')

