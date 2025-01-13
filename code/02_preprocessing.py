# import library yang digunakan 
import pandas as pd     # import library untuk pengolahan dataframe 
import numpy as np      # import library untuk komputasi numerik 
import warnings         # import library untuk handing error 

from sklearn.preprocessing import LabelEncoder      # import library untuk konversi tipe data kaegorik ke numerik 
from sklearn.preprocessing import StandardScaler    # import library untuk normalisasi z-score untuk kolom fitur pendapatan tahunan dan skor pengeluaran
from scipy.stats.mstats import winsorize            # import library untuk preprocesing outliers

# buat variabel untuk menghilangkan error pada saat 
warnings.filterwarnings('ignore')

# load datasheet yang digunakan 
df = pd.read_csv('../data/Mall_Customers.csv')

# hilangkan outliers dari kolom fitur pendapatab tahuhanan dan skor pengeluaran 

