# import library yang dibutuhkan 
import numpy as np   # import library untuk komputasi numerik dengan numpy 
import pandas as pd  # import library untuk pengolahan dataframe dengan pandas 
import warnings      # import library untuk penanganan error 
import joblib        # import library untuk load model ke dlaam format joblib 

from sklearn.cluster import KMeans  # import library untuk pembuatan model k-means 

# buat variabel untuk handling error yang terjadi pada saat proses komputasi 
warnings.filterwarnings('ignore')

# load datasheet yang sudah di proprocessing sebelum nya 
df = pd.read_csv('../data/hasil_transformasi.csv')

# cari nilai k yang optimal karena dalam hal ini nilai k 
wcss = []
for i in range(1,11):
    model = KMeans(n_clusters = i, init='k-means++', random_state=0)
    model.fit(df)
    wcss.append(model.inertia_)

# buat variabel untuk menguji data dengan model k-means yang berjumlah 5
k_means = KMeans(n_clusters = 5).fit(df)

# load datasheet untuk digabungan dengan hasil k-means 
data = pd.read_csv('../data/Mall_Customers.csv')

# simpan kategori hasil klaster ke kolom df 
data['klaster'] = k_means.labels_

# tampilkan hasil dari model K-Means 
print(data.head())

# simpan file hasil transformasi ke dalam bentuk format csv 
data.to_csv('../data/kmeans.csv', index=False)

# Simpan model 
joblib.dump(k_means, '../models/kmeans model/kmeans_model.pkl')
