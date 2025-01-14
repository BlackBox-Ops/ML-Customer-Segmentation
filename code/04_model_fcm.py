# import library yang dibutuhkan 
import pandas as pd     # library untuk pengolahan dataframe 
import warnings         # library untuk handling error 
import numpy  as np     # library untuk proses komputasi numerik 

# library untuk model fuzzy c-means 
from fcmeans import FCM

# buat variabel untuk handling error pada saat run program 
warnings.filterwarnings('ignore')

# load datasheet yang sudah di normalisasi sebelum nya dengan pandas 
df = pd.read_csv('../data/hasil_transformasi.csv')

# pisahkan kolom fitur x dan rubah ke tipe data array 
X = df.iloc[:, :4]  # memilih semua kolom pada datasheet yang sudah di transformasi 
X = np.array(X)     # transformasi kolom X ke dalam bentuk array 

# buat model fuzzy c-means 
model_c_means = FCM(n_clusters=5)
