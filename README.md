# Exploratory Data Analysis - Mall Customer Segmentation

## Deskripsi Proyek

Proyek ini merupakan studi analisis eksploratif data (EDA) pada data pelanggan Mall, yang bertujuan untuk mengidentifikasi pola konsumen berdasarkan berbagai fitur seperti:
- Jenis Kelamin
- Usia dan Kategori Usia
- Pendapatan Tahunan
- Skor Pengeluaran

Analisis ini dilakukan untuk memberikan insight yang dapat digunakan dalam strategi segmentasi pelanggan dan peningkatan penjualan.

---

## Struktur Notebook

### 1. Koneksi ke Database PostgreSQL
Menggunakan pendekatan OOP (Object-Oriented Programming) untuk menghubungkan ke database PostgreSQL dan mengambil data dari tabel `customer_segmentation`.

### 2. Pemeriksaan Awal Data
- Menampilkan beberapa data awal
- Mengecek jumlah baris dan kolom
- Menangani missing value dan duplikasi

### 3. Preprocessing
- Rename nama kolom agar lebih mudah dibaca
- Penyesuaian tipe data jika diperlukan

### 4. Visualisasi dan Analisis Statistik
- Boxplot untuk deteksi outlier
- Grouping berdasarkan kategori usia dan jenis kelamin
- Pemetaan visual berdasarkan pengeluaran dan pendapatan

---

## Tools dan Library
- Python 3
- pandas, numpy
- seaborn, matplotlib
- psycopg2 untuk koneksi PostgreSQL

---

## Cara Menjalankan
1. Pastikan environment Python Anda sudah terinstall dependency yang dibutuhkan.
2. Pastikan PostgreSQL sudah berjalan dan memiliki tabel `customer_segmentation`.
3. Jalankan file notebook untuk memuat dan memproses data.

---

## Output yang Diharapkan
Insight segmentasi pelanggan berdasarkan:
- Kategori usia
- Pengeluaran tinggi dan rendah
- Pendapatan tinggi dan rendah
- Perbedaan perilaku berdasarkan gender

---

## Dokumentasi Teknis Tambahan

- **Struktur Tabel Database**:
  - `customer_segmentation(CustomerID, Gender, Age, Annual_Income(k$), Spending_Score(1-100), kategori_usia)`
- **Kategori Usia**:
  - Dibentuk secara custom berdasarkan range usia
  - Contoh: `Dewasa Muda`, `Dewasa`, `Paruh Baya`, `Lansia`
- **Transformasi Nama Kolom**:
  - `Annual Income (k$)` menjadi `Pendapatan_Tahunan`
  - `Spending Score (1-100)` menjadi `Skor_Pengeluaran`

- **Boxplot**:
  - Digunakan untuk mendeteksi outlier pada `Pendapatan_Tahunan` dan `Skor_Pengeluaran`
  
- **Pendekatan Segmentasi**:
  - Pendekatan statistik berbasis pengelompokan visual
  - Bisa dikembangkan ke clustering model (KMeans, DBSCAN) ke depannya

---

## Kontribusi

Kontribusi sangat terbuka! Jika Anda memiliki ide perbaikan, tambahan fitur, atau perbaikan dokumentasi, silakan:
1. Fork repositori ini
2. Buat branch baru (`feature/fitur-baru`)
3. Lakukan perubahan dan commit
4. Ajukan pull request

---

## Lisensi

Proyek ini dilisensikan di bawah [MIT License](LICENSE).  
Silakan gunakan, modifikasi, atau distribusikan dengan tetap mencantumkan atribusi kepada pemilik asli proyek.

---

