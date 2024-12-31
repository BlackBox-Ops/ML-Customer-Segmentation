# Rumus untuk Menghitung Persentase Jenis Kelamin Berdasarkan Kategori Usia

Untuk menghitung persentase dari jenis kelamin dalam suatu kategori usia, kita bisa menggunakan rumus sebagai berikut:

$$
\text{Persentase Gender} = \left( \frac{\text{Jumlah Pelanggan dengan Gender Tertentu}}{\text{Total Pelanggan dalam Kategori Usia}} \right) \times 100
$$

## Keterangan Variabel
1. **Persentase Gender**  
   - Nilai persentase yang ingin kita hitung.  
   - Contohnya, persentase pelanggan **Perempuan** dalam kategori usia **Dewasa Muda**.
    
2. **Jumlah Pelanggan dengan Gender Tertentu**  
   - Total pelanggan dengan gender tertentu (misalnya **Laki-Laki** atau **Perempuan**) dalam kategori usia tertentu.

3. **Total Pelanggan dalam Kategori Usia**  
   - Total keseluruhan pelanggan dalam kategori usia tertentu (termasuk semua gender).

4. **× 100**  
   - Digunakan untuk mengubah hasil menjadi format persentase.

## Contoh Kasus
Misalkan data berikut:

| Kategori Usia | Gender  | Jumlah Pelanggan |
|---------------|---------|------------------|
| Dewasa Muda   | Male    | 30               |
| Dewasa Muda   | Female  | 20               |
| Dewasa        | Male    | 25               |
| Dewasa        | Female  | 25               |

*Tabel di atas hanya merupakan gambaran perhitungan dari datasheet yang kita gunakan.*

### Hitung Persentase Jenis Kelamin Perempuan di Kategori Dewasa Muda
1. Jumlah pelanggan **Female** (Dewasa Muda) = 20  
2. Total pelanggan (Dewasa Muda) = 30 (Male) + 20 (Female) = 50  

Berikut ini adalah perhitungannya:

$$
\text{Persentase Gender (Female, Dewasa Muda)} = \left( \frac{20 \times 100}{50} \right) = 40\%
$$

### Implementasi dengan SQL
Kita bisa mengimplementasikan perhitungan di atas menggunakan query SQL sebagai berikut:

1. **Jumlah Pelanggan dengan Gender Tertentu**:  
   `COUNT(*) WHERE "Gender" = 'female' AND kategori_usia = 'Dewasa Muda'`

2. **Total Pelanggan dalam Kategori Usia**:  
   `SUM(COUNT(*)) OVER (PARTITION BY kategori_usia)`

3. **SQL Query**:
   ```sql
   SELECT 
       "Gender",
       "kategori_usia",
       ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY "kategori_usia"), 2) AS persentase
   FROM customer_segmentation
   GROUP BY "kategori_usia", "Gender";
   ```