# import library yang dibutuhkan 
import pandas as pd     # library untuk pengolahan dataframe 
import warnings         # library untuk handling error 
import numpy  as np     # library untuk proses komputasi numerik 
import joblib           # library untuk load model yang sudah jadi kedalam format joblib

# library untuk model fuzzy c-means 
from fcmeans import FCM

# buat variabel untuk handling error pada saat run program 
warnings.filterwarnings('ignore')

# load datasheet yang sudah di normalisasi sebelum nya dengan pandas 
df = pd.read_csv('../data/hasil_transformasi.csv')

# pisahkan kolom fitur x dan rubah ke tipe data array 
X = df.iloc[:, :4]  # memilih semua kolom pada datasheet yang sudah di transformasi 
X = np.array(X)     # transformasi kolom X ke dalam bentuk array 

# buat model fuzzy c-means dan atur jumlah nila k sebesar 4, parameter fuzzy 2.0, jumlah iterasi 150 
model_c_means = FCM(n_clusters=4, m=2.0, max_iter=150, error=1e-5, random_state=42)

# masukan variabel X dan uji dengan variabel model c-means
model_c_means.fit(X)

#  tentukan titik tengah dari masing-masing cluster 
centers = model_c_means.centers

# buat label cluster dan prediksi terhadap nilai X
labels  = model_c_means.predict(X)

# load datasheet untuk digabungan dengan hasil k-means 
data = pd.read_csv('../data/kmeans.csv')

# simpan hasil klaster ke c-means 
data['C-means'] = labels
print(df)

# simpan file hasil transformasi ke dalam bentuk format csv 
data.to_csv('../data/cmeans.csv', index=False)

# Simpan model dan scaler
joblib.dump(model_c_means, '../models/cmeans model/cmeans_model.pkl')
