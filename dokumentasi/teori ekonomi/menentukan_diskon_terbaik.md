# Rumus untuk Menentukan Diskon Terbaik

Diskon terbaik dapat dihitung dengan mempertimbangkan beberapa variabel: **kategori usia**, **usia**, **gender**, **pendapatan tahunan**, dan **skor pengeluaran**. Kita akan menggabungkan variabel-variabel tersebut untuk menentukan **nilai prioritas** *(P)* yang kemudian akan digunakan untuk menetapkan besar diskon *(D)*.

## 1. Rumus Menentukan Prioritas Diskon untuk Customer Segmentation

Berikut ini adalah rumus untuk menentukan prioritas diskon untuk segmentasi pelanggan berdasarkan kategori usia, pendapatan tahunan, dan skor pengeluaran:

$$
P = W_1 \cdot K + W_2 \cdot U + W_3 \cdot G + W_4 \cdot (1 - I) + W_5 \cdot (1 - S)
$$

## 2. Penjelasan Variabel

Berikut adalah variabel yang digunakan untuk menghitung prioritas diskon berdasarkan kategori usia, jenis kelamin, dan faktor lainnya.

### 1. Kategori Usia

Kategori usia diberi skor sebagai berikut:

$$ 
k = 
\begin{cases} 
1 & \text{Remaja} (\leq 18 \text{ Tahun}) \\
0.8 & \text{Dewasa Muda} (19-30 \text{ Tahun}) \\
0.6 & \text{Dewasa} (31-60 \text{ Tahun}) \\
0.4 & \text{Pensiun} (>60 \text{ Tahun})
\end{cases}
$$

- **Alasan**: Remaja diberi prioritas tinggi karena lebih terpengaruh oleh diskon, sedangkan kelompok pensiun lebih rendah karena daya beli stabil.

### 2. Usia *(U)*

Tahap selanjutnya adalah normalisasi umur ke rentang [0,1]:

$$
U = \frac{\text{Usia}}{\text{Usia Maksimum}}
$$

### 3. Gender *(G)*

Gender dapat mempengaruhi respons terhadap diskon. Contoh:

$$
G = 
\begin{cases} 
1 & \text{Perempuan (lebih responsif terhadap diskon)} \\
0.8 & \text{Laki-Laki}
\end{cases}
$$

### 4. Pendapatan Tahunan *(I)*

Semakin tinggi pendapatan, semakin kecil prioritas diskon:

$$
I = \frac{\text{Pendapatan Tahunan}}{\text{Pendapatan Maksimum}}
$$

### 5. Skor Pengeluaran *(S)*

Semakin tinggi skor pengeluaran, semakin rendah prioritas diskon:

$$
S = \frac{\text{Skor Pengeluaran}}{100}
$$

### 6. Bobot *(W)*

Bobot diberikan sesuai dengan kepentingan. Contoh:

- \( W_1 = 0.3 \) (Kategori Usia)
- \( W_2 = 0.2 \) (Usia)
- \( W_3 = 0.1 \) (Gender)
- \( W_4 = 0.2 \) (Pendapatan)
- \( W_5 = 0.2 \) (Pengeluaran)

### 7. Rumus Diskon

Setelah menghitung nilai prioritas *(P)*, besar diskon *(D)* dapat ditentukan dengan rumus:

$$
D = D_{\text{max}} \cdot P
$$

**Penjelasan**:

- \( D_{\text{max}} \) = Diskon maksimum yang tersedia untuk produk (misalnya 50%)
- \( P \) = Nilai prioritas yang dihitung dari rumus di atas, dengan nilai maksimum.

## Contoh Kasus

Misalkan data pelanggan sebagai berikut:

- Kategori Usia = Dewasa muda (19-30 tahun)
- Usia = 25 tahun 
- Jenis Kelamin: Perempuan 
- Pendapatan Tahunan: 50.000 (dari maksimum 100.000) 
- Skor Pengeluaran: 60 (dari maksimum 100)

**Perhitungan**:

1. Kategori Usia:

$$
K = 0.8
$$

2. Usia *(U)*:

$$
U = \frac{25}{60} = 0.42
$$

3. Gender *(G)*:

$$
G = 1 \quad (\text{Perempuan})
$$

4. Pendapatan *(I)*:

$$
I = \frac{50,000}{100,000} = 0.5
$$

5. Nilai Prioritas *(P)*:

$$
P = (0.3 \cdot 0.8) + (0.2 \cdot 0.42) + (0.1 \cdot 1) + (0.2 \cdot (1 - 0.5)) + (0.2 \cdot (1 - 0.6))
$$

$$
P = 0.24 + 0.084 + 0.1 + 0.1 + 0.08 = 0.604
$$

6. Nilai Diskon *(D)*:

$$
D = 50 \cdot 0.604 = 30.2\%
$$

## 8. Jika Ingin Menghitung dengan SQL

```sql
SELECT 
    "CustomerID",
    "Gender",
    "Age",
    "Annual Income (k$)",
    "Spending Score (1-100)",
    "kategori_usia",
    ROUND(
        (0.3 * 
            CASE 
                WHEN "kategori_usia" = 'Remaja' THEN 1 
                WHEN "kategori_usia" = 'Dewasa Muda' THEN 0.8 
                WHEN "kategori_usia" = 'Dewasa' THEN 0.6 
                ELSE 0.4 
            END
        ) + 
        (0.2 * ("Age" / (SELECT MAX("Age") FROM customer_segmentation))) + 
        (0.1 * 
            CASE 
                WHEN "Gender" = 'Female' THEN 1 
                ELSE 0.8 
            END
        ) + 
        (0.2 * (1 - ("Annual income (k$)" / (SELECT MAX("Annual income (k$)") FROM customer_segmentation)))) + 
        (0.2 * (1 - ("Spending Score (1-100)" / 100))), 4
    ) AS prioritas_diskon,
    ROUND(50 * (
        (0.3 * 
            CASE 
                WHEN "kategori_usia" = 'Remaja' THEN 1 
                WHEN "kategori_usia" = 'Dewasa Muda' THEN 0.8 
                WHEN "kategori_usia" = 'Dewasa' THEN 0.6 
                ELSE 0.4 
            END
        ) + 
        (0.2 * ("Age" / (SELECT MAX("Age") FROM customer_segmentation))) + 
        (0.1 * 
            CASE 
                WHEN "Gender" = 'Female' THEN 1 
                ELSE 0.8 
            END
        ) + 
        (0.2 * (1 - ("Annual Income (k$)" / (SELECT MAX("Annual income") FROM customer_segmentation)))) + 
        (0.2 * (1 - ("Spending Score (1-100)" / 100)))
    ), 2) AS diskon
FROM customer_data;
