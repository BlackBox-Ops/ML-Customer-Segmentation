import pandas as pd
import psycopg2
from sqlalchemy import create_engine

# 1. Membaca file CSV
csv_file = '../data/Mall_Customers.csv'  # Ganti dengan path file CSV Anda
df = pd.read_csv(csv_file)

# 2. Menyambung ke Database PostgreSQL
# Pastikan Anda mengganti parameter sesuai dengan kredensial PostgreSQL Anda
db_params = {
    'host': 'localhost',
    'dbname': 'DB_ML',
    'user': 'postgres',
    'password': 'admin',
    'port': 5432  # default PostgreSQL port
}

# Membuat engine untuk koneksi menggunakan sqlalchemy
engine = create_engine(f'postgresql://{db_params["user"]}:{db_params["password"]}@{db_params["host"]}:{db_params["port"]}/{db_params["dbname"]}')

# 3. Menyimpan DataFrame ke PostgreSQL
# Ganti 'nama_tabel' dengan nama tabel yang diinginkan di database PostgreSQL
df.to_sql('customer_segmentation', engine, index=False, if_exists='replace')  # 'replace' akan menggantikan tabel jika ada

print("Data berhasil disimpan ke PostgreSQL!")
