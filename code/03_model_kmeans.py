# import library yang dibutuhkan 
import numpy as np   # import library untuk komputasi numerik dengan numpy 
import pandas as pd  # import library untuk pengolahan dataframe dengan pandas 
import warnings      # import library untuk penanganan error 

from sklearn.cluster import KMeans  # import library untuk pembuatan model k-means 
from yellowbrick.cluster import kelbow_visualizer # import library untuk menentuka nilai k optimal untuk model k-means 

# load datasheet yang sudah di proprocessing sebelum nya 
df = pd.read_csv()