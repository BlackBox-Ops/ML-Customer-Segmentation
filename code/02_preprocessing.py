# import library yang digunakan 
import pandas as pd   # import library untuk pengolahan dataframe   
import numpy as np    # import library untuk komputasi numerik 
import warnings       # import library untuk handing error 

from sklearn.preprocessing import LabelEncoder   # import library untuk konversi tipe data kaegorik ke numerik 
from sklearn.preprocessing import StandardScaler # import library untuk normalisasi z-score untuk kolom fitur pendapatan tahunan dan skor pengeluaran
from scipy.stats.mstats import winsorize         # import library untuk preprocesing outliers 

# buat variabel untuk menghilangkan error pada saat 
warnings.filterwarnings('ignore')

# load datasheet yang digunakan 
df = pd.read_csv('../data/Mall_Customers.csv')

# hilangkan outliers dari kolom fitur pendapatan tahuhanan dan skor pengeluaran 
df['Annual Income (k$)'] = winsorize(df['Annual Income (k$)'], limits=[0.05, 0.05])
df['Spending Score (1-100)'] = winsorize(df['Spending Score (1-100)'], limits=[0.05, 0.05])

# menghapus kolom Customer ID 
df.drop(['CustomerID'], axis=1, inplace=True)

# buat variabel untuk transformasi data kategorik menggunakan label encoder
Label = LabelEncoder()

# transformasi kolom dengan tipe data kategorik ke bentuk numerik dengan label encoder
df['Gender'] = Label.fit_transform(df['Gender'])

# buat variabel untuk transformasi dan normalisasi data tipe data numerik dengan standard score 
scaler = StandardScaler()

Gender = df['Gender'] # pisahkan kolom gender 
df.drop('Gender', axis=1)

# buat dataframe hasil normalisasi data 
df = pd.DataFrame(scaler.fit_transform(df), columns= df.columns)
df['Gender'] = Gender
print(df.head())

# simpan file hasil transformasi ke dalam bentuk format csv 
df.to_csv('../data/hasil_transformasi.csv', index=False)