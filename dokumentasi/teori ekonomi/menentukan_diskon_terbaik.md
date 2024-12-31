# Rumus untuk menentukan diskon terbaik 

Diskon terbaik dapat dihitung dengan mempertimbangkan beberapa variabel : **kategori usia**, **usia**, **gender** **pendapatan tahunan** dan **skor pengeluaran** kita akan menggabungkan  variabel-variabel tersebut untuk menentukan **nilai prioritas** *(P)* yang kemudian akan digunakan untuk menetapkan besar diskon *(D)*.

## 1. Rumus menentukan prioritas diskon untuk customer segmentation 
Berikut ini adalah rumus untuk menentukan prioritas diskon untuk segmentasi pelanggan berdasarkan kategori usia dan pendapatan tahunan serta skor pengeluaran.

$$
P = W_1 \cdot K + W_2 \cdot U + W_3 \cdot G + W_4 \cdot (1 - I) + W_5 \cdot (1 - S)
$$

 ## 2. Penjelasan Variabel 
 Berikut ini adalah variabel yang digunakan untuk menghitung prioritas diskon berdasarkan kategori usia dan jenis kelamin.

 1. **Kategori usia**
    - kategori usia diberi sekor sebagai berikut : 
    $$ 
    k = \left\{
    \begin{array}{ll}
    1 & \text{Remaja} (\leq 18 \text{ Tahun}) \\
    0.8 & \text{Dewasa Muda} (19-30 \text{ Tahun}) \\
    0.6 & \text{Dewasa} (31-60 \text{ Tahun}) \\
    0.4 & \text{Pensiun} (>60 \text{ Tahun})
    \end{array}
    \right.
    $$
 
  - **Alasan** : Remaja diberi priritas tinggi karena lebih terpengaruh oleh diskon, sedangkan kelompok pensiun lebih rendah karena daya beli stabil.
 
 2. **Usia *(U)***
    - Tahap selanjutnya adalah normalisasi umur ke rentang [0,1] :
    $$
    U = \frac{\text{Usia}}{\text{Usia Maksimum}}
    $$

 3. **Gender *(G)***
    - Gender dapat memperngaruhi respons terhadap diskon. Contoh : 
    $$
    G = \left\{
    \begin{array}{ll}
    1 & \text{Perempuan (lebih responsif terhadap diskon)} \\
    0.8 & \text{Laki-Laki}
    \end{array}
    \right.
    $$
 
 4. **Pendapatan Tahunan *(I)***
    - Semakin tinggi pendapatan semakin kecil prioritas diskon :
    $$
    I = \frac{\text{Pendapatan Tahunan}}{\text{Pendapatan Maksimum}}
    $$
 
 5. **Skor Pengeluaran *(S)***
    - Semakin tinggi skor pengeluaran, semakin rendah prioritas diskon : 
    $$
    S = \frac{\text{Skor Pengeluaran}}{\text{100}}
    $$
 
 6. **Bobot *(W)***
    - Bobot diberikan sesuai dnegan kepentingan. Contoh : 
    - W1 = 0.3 (Kategori Usia)
    - W2 = 0.2 (Usia)
    - W3 = 0.1 (Gender)
    - W4 = 0.2 (Pendapatan)
    - W5 = 0.2 (Pengeluaran)
 
 7. **Rumus Diskon**
    - Setelah menghitung nilai prioritas *(P)*, besar diskon *(D)* dapat ditentukan dengan rumus :

    $$
    D = D_{\text{max}} \cdot P
    $$

    **penjelasan :**
    - D max = Diskon maksimum yang tersedia untuk produk (misalnya 50%)
    - P = Nilai prioritas yang dihitung dari rumus di atas, dengan nilai maksimum 1.


## Contoh kasus :
Misalkan data pelanggan sebagai berikut :

- Kategori Usia = Dewasa muda (19-30 tahun)
- Usia = 25 tahun 
- Jenis Kelamnin : Perempuan 
- Pendapatan Tahunan : 50.000  (dari maksimum $ 100.000) 
- Skor pengeluaran 60 (dari maksimum 100)

**perhitungan :**
 1 Kategori Usia :
 $$
    K= 0.8
 $$

 2. Usia (U) :
  $$
    U = \frac{\text{25}}{\text{60}} = 0.42
  $$

 3.  Gender (G) :
 $$
    G = 1 (Female)
 $$

 4. Pendapatan :
 $$
    I = \frac{\text{50,000}}{\text{100,00}} = 0.5
 $$

 5. Nilai Prioritas (P) :
 $$
   P = (0.3 \cdot 0.8) + (0.2 \cdot 0.42) + (0.1 \cdot 1) + (0.2 \cdot (1 - 0.5)) + (0.2 \cdot (1 - 0.6))
 $$

 $$
    P =0.24 + 0.084 + 0.1 + 0.1 + 0.08 = 0.604
 $$

 6. Nilai Prioritas (P)
 $$
    D = 50 \cdot  0.604 = 30.2 \%
 $$

 7. Jika ingin menghitung dengan SQL
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
 ```