# Rumus untuk menghitung persentase jenis kelamin berdasarkan kategori usia

Untuk untuk menghitung persentase dari jenis kelamin dalam suatu kategori usia kita bisa menggunakan perhitungan jumlah pelanggan tertentu dikali 100 dan dibagi dengan total pelanggan dalam kategori usia. 

Berikut ini adalah notasi matematika nya :
\[
\text{Persentase Gender} = \left( \frac{\text{Jumlah Pelanggan dengan Gender Tertentu}}{\text{Total Pelanggan dalam Kategori Usia}} \right) \times 100
\]

## Keterangan Variabel
1. Persentase Gender
    - nilai persentase yang ingin kita hitung 
    - contohnya, persentase pelanggan **Perempuan** dalam kategori usia **dewasa muda**.
    
2. Jumlah pelanggan dengan gender tertentu :
    - Total pelanggan dengan gender tertentu (misalnya **laki-laki** atau **perempuan**) dalam kategori usia tertentu. 

3. Total pelanggan dalam Kategori Usia
    - Total keseluruhan pelanggan dalam kategori usia tertentu (termasuk semua gender)

4. x 100 : 
   -  Digunakan untuk merubah hasil menjadi format persentase 

## Contoh Kasus : 
Misalkan data berikut

|Kategori Usia|Gender  |Jumlah Pelanggan|
|-------------|--------|----------------|
|Dewasa Muda  | Male   | 30             |
|Dewasa Muda  | Female | 20             |
|Dewasa       | Male   | 25             |
|Dewasa       | Female | 25             |

*Tabel diatas hanya merupakan gambaran perhitunngan dari datasheet yang kita gunakan*

#### Hitung persentase jenis kelamin perempuan di kategori dewasa muda :
1. Jumlah pelanggan female (dewasa muda) = 20
2. Total Pelanggan (Dewasa Muda) = 30 (Male) + 20 (Female) = 50

Berikut ini adalah contoh perhitungan nya :

\[
\text{Persentase Gender (Female, Dewasa Muda)} = \left( \frac{20 \times 100}{50} \right) = 40\%
\]

Kita bisa implementasikan perhitungan diatas menggunakan Query SQL sebagai berikut :
1. Jumlah Pelanggan dengan Gender Tertentu : 
    - `COUNT(*) WHERE "Gender" = 'female' AND kategori_usia = 'Dewasa Muda' `
2. Total Pelanggan dalam kategori Usia :
    - `SUM(COUNT(*)) OVER (PARTITION BY kategori_usia)`
3. SQL Query
    ```sql
    SELECT 
        "Gender",
        "kategori_usia",
        ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY "kategori_usia"), 2) AS persentase
    FROM customer_segmentation
    GROUP BY "kategori_usia", "Gender";
    ```


 