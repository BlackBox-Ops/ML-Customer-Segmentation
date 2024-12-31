-- Create table customer segmentation 
CREATE TABLE customer_segmentation (
	CustomerID SERIAL PRIMARY KEY,
	Gender VARCHAR(10) NOT NULL, 
	AGE INTEGER NOT NULL,
	Annual_income INTEGER NOT NULL, 
	Spending_score INTEGER NOT NULL
);

-- lihat isi dari table customer 
SELECT * FROM customer_segmentation;

SELECT "CustomerID","Gender", "Age", "Annual Income (k$)", "Spending Score (1-100)"
	FROM public.customer_segmentation;

SELECT * FROM public.customer_segmentation
LIMIT 100

-- 	Analisis distribusi gender 
SELECT "Gender", COUNT(*) AS jumlah_pelanggan
FROM customer_segmentation
GROUP BY "Gender";

-- Analisis Rata-rata Penghasilan Berdasarkan Gender
SELECT "Gender", ROUND(AVG("Annual Income (k$)")) AS rata_rata_penghasilan
FROM customer_segmentation
GROUP BY "Gender";

-- Analisis Pengeluaran berdasarkan gender 
SELECT "Gender", ROUND(AVG("Spending Score (1-100)")) AS rata_rata_pengeluaran
FROM customer_segmentation
GROUP BY "Gender";

-- Analisis rata-rata pendapatan dan pengeluaran berdasarkan gender 
SELECT "Gender",
    ROUND(AVG("Annual Income (k$)")) AS avg_income,
    ROUND(AVG("Spending Score (1-100)")) AS avg_score
FROM 
customer_segmentation 
GROUP BY "Gender";

-- Analisis Distribusi usia 
SELECT "Age", COUNT(*) AS Jumlah
FROM customer_segmentation
GROUP BY "Age"
ORDER BY "Age";

-- Rata - Rata pengeluaran dan pendapatan berdasarkan kelompok usia 
SELECT 
	CASE
         WHEN "Age" BETWEEN 18 AND 25 THEN '18-25'
         WHEN "Age" BETWEEN 26 AND 35 THEN '26-35'
         WHEN "Age" BETWEEN 36 AND 45 THEN '36-45'
         WHEN "Age" BETWEEN 46 AND 55 THEN '46-55'
         ELSE '56+'
       END AS age_group,
       ROUND(AVG("Annual Income (k$)")) AS avg_income, 
	   ROUND(AVG("Spending Score (1-100)")) AS avg_score
FROM customer_segmentation
GROUP BY age_group;

-- Analisis korelasi pendapatan dan pengeluaran
SELECT 
	"Annual Income (k$)", 
	ROUND(AVG("Spending Score (1-100)")) AS rata_rata_spending_score
FROM customer_segmentation
GROUP BY "Annual Income (k$)"
ORDER BY "Annual Income (k$)";

-- Korelasi pendapatan dan pengeluaran 
SELECT 
	CASE
		WHEN "Annual Income (k$)" BETWEEN 0 AND 30000 THEN 'Low Income'
        WHEN "Annual Income (k$)" BETWEEN 30001 AND 60000 THEN 'Middle Income'
        ELSE 'High Income'
    END AS income_group,
       ROUND(AVG("Spending Score (1-100)")) AS avg_score
FROM customer_segmentation
GROUP BY income_group;

-- Analisis distribusi penghasilan 
SELECT 
	CASE 
		WHEN "Annual Income (k$)" < 20000 THEN 'Low Income (< 20k)'
		WHEN "Annual Income (k$)" BETWEEN 20000 AND 50000 THEN 'Middle Income (20k-50k)'
		ELSE 'High Income (>50k)'
	END AS income_group,
	COUNT(*) AS jumlah_pelanggan
FROM customer_segmentation
GROUP BY income_group 
ORDER BY income_group;

-- Analisis Spending Score 
SELECT 
	CASE 
		WHEN "Age" < 20 THEN 'Below 20'
		WHEN "Age" BETWEEN 20 AND 30 THEN '20 - 30'
		WHEN "Age" BETWEEN 31 AND 40 THEN '31 - 40'
		WHEN "Age" BETWEEN 41 AND 50 THEN '41 - 50'
		ELSE 'Above 50'
	END AS age_group,
	ROUND(AVG("Spending Score (1-100)")) AS rata_rata_spending_score
FROM customer_segmentation 
GROUP BY age_group
ORDER BY age_group;

-- Analisis pelanggan dengan spending score tertinggi 
SELECT 
	"Gender", 
	"Age", 
	"Annual Income (k$)", 
	"Spending Score (1-100)" 
FROM customer_segmentation 
ORDER BY "Spending Score (1-100)" DESC
LIMIT 10;

-- Analisis pelanggan dengan pendapatan tertinggi 
SELECT 
	"Gender", 
	"Age",
	"Annual Income (k$)",
	"Spending Score (1-100)"
FROM customer_segmentation 
ORDER BY "Annual Income (k$)" DESC
LIMIT 10;

-- Analisis spending score berdasarkan gender 
SELECT "Gender", ROUND(AVG("Spending Score (1-100)")) as rata_rata_spending_score
FROM customer_segmentation 
GROUP BY "Gender";

SELECT 
    gender_analysis.gender,
    gender_analysis.rata_rata_spending_score_gender,
    age_analysis.age_group,
    age_analysis.rata_rata_spending_score_age
FROM 
    ( -- Subquery 1: Analisis Spending Score Berdasarkan Gender
        SELECT 
            "Gender" AS gender,
            ROUND(AVG("Spending Score (1-100)")) AS rata_rata_spending_score_gender
        FROM customer_segmentation
        GROUP BY "Gender"
    ) AS gender_analysis
CROSS JOIN
    ( -- Subquery 2: Analisis Spending Score Berdasarkan Usia
        SELECT 
            CASE 
                WHEN "Age" < 20 THEN 'Below 20'
                WHEN "Age" BETWEEN 20 AND 30 THEN '20 - 30'
                WHEN "Age" BETWEEN 31 AND 40 THEN '31 - 40'
                WHEN "Age" BETWEEN 41 AND 50 THEN '41 - 50'
                ELSE 'Above 50'
            END AS age_group,
            ROUND(AVG("Spending Score (1-100)")) AS rata_rata_spending_score_age
        FROM customer_segmentation
        GROUP BY age_group
    ) AS age_analysis
ORDER BY gender_analysis.gender, age_analysis.age_group;

-- membuat kolom baru dengan nama kategori usia 
ALTER TABLE customer_segmentation ADD COLUMN kategori_usia VARCHAR(20);
UPDATE customer_segmentation 
SET kategori_usia = CASE
	WHEN "Age" <= 18 THEN 'Remaja'
	WHEN "Age" BETWEEN 19 AND 30 THEN 'Dewasa Muda'
	WHEN "Age" BETWEEN 31 AND 60 THEN 'Dewasa'
	ELSE 'Pensiun'
END;

SELECT * FROM customer_segmentation;

-- kategorisasi usia 
CREATE VIEW kelompok_belanja AS
SELECT 
	"Gender",
	"kategori_usia",
	COUNT("CustomerID") AS jumlah_pelanggan 
FROM (
	SELECT 
		"CustomerID",
		"Gender",
		CASE 
			WHEN "Age" <= 18 THEN 'Remaja'
			WHEN "Age" BETWEEN 19 AND 30 THEN 'Dewasa Muda'
			WHEN "Age" BETWEEN 31 AND 60 THEN 'Dewasa'
			ELSE 'Pensiun'
		END AS "kategori_usia"
	FROM customer_segmentation 
) AS categorized_data 
GROUP BY "Gender", "kategori_usia";

SELECT * FROM kelompok_belanja;

-- gunakan window cte untuk analisis customer yang paling banyak melakukan pembelian berdasarkan usia 
WITH daya_beli_customer AS (
	SELECT 
		"kategori_usia", 
		SUM("Annual Income (k$)") AS total_pendapatan_tahunan,
		SUM("Spending Score (1-100)") AS total_pengeluaran_tahunan
	FROM customer_segmentation 
	GROUP BY "kategori_usia"
)

-- mengurutkan hasil berdasarkan pendapatan tahunan, skor pengeluaran
SELECT 
	"kategori_usia",
	"total_pendapatan_tahunan",
	"total_pengeluaran_tahunan"
FROM daya_beli_customer
ORDER BY
	"total_pendapatan_tahunan" DESC,
	"total_pengeluaran_tahunan" DESC
LIMIT 5;

SELECT * FROM daya_beli_customer;

-- membuat trigger untuk mengurutkan kategori usia

CREATE OR REPLACE FUNCTION categorize_age_trigger()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW."Age" <= 18 THEN
        NEW.kategori_usia := 'Remaja';
    ELSIF NEW."Age" BETWEEN 19 AND 30 THEN
        NEW.kategori_usia := 'Dewasa Muda';
    ELSIF NEW."Age" BETWEEN 31 AND 60 THEN
        NEW.kategori_usia := 'Dewasa';
    ELSE
        NEW.kategori_usia := 'Pensiun';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- memuat triger untuk mengisi kategori usia
CREATE TRIGGER set_kategori_usia
BEFORE INSERT OR UPDATE ON customer_segmentation
FOR EACH ROW
EXECUTE FUNCTION categorize_age_trigger();

-- memuat view untuk persentase jenis kelamin 
CREATE OR REPLACE VIEW gender_percentage_by_age_group AS
SELECT 
    kategori_usia,
    "Gender",
	CONCAT(ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY kategori_usia), 2), '%') AS persentase
FROM customer_segmentation
GROUP BY kategori_usia, "Gender";

-- membuat trigger function untuk menyimpan persentase 
CREATE OR REPLACE FUNCTION update_gender_percentage_trigger()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO gender_percentage (kategori_usia, gender, persentase)
    SELECT 
        kategori_usia,
        "Gender",
        CONCAT(ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY kategori_usia), 2), '%') AS persentase
    FROM customer_data
    GROUP BY kategori_usia, "Gender"
    ON CONFLICT (kategori_usia, gender) DO UPDATE
    SET persentase = EXCLUDED.persentase;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

SELECT * FROM gender_percentage_by_age_group;

-- analisis persentase konsumen loyal berdasarkan gender dan kategori usia 
SELECT 
    "CustomerID",
    "Gender",
    "Age",
    CASE 
        WHEN "Age" <= 18 THEN 'Remaja'
        WHEN "Age" BETWEEN 19 AND 30 THEN 'Dewasa Muda'
        WHEN "Age" BETWEEN 31 AND 60 THEN 'Dewasa'
        ELSE 'Pensiun'
    END AS "Kategori Usia"
FROM customer_segmentation;

WITH Frekuensi AS (
    SELECT 
        "CustomerID", 
        "Gender", 
        "kategori_usia", 
        COUNT(*) AS "Frekuensi Interaksi"
    FROM customer_segmentation
    GROUP BY "CustomerID", "Gender", "kategori_usia"
)
SELECT AVG("Frekuensi Interaksi") AS rata_rata_frekuensi
FROM Frekuensi;

SELECT * FROM customer_segmentation;

SELECT * FROM kelompok_belanja;

CREATE VIEW Resiko AS (
	SELECT 
		"CustomerID",
		"Gender",
		"Age",
		"Annual Income (k$)", 
		"Spending Score (1-100)", 
		"kategori_usia",
		ROUND((0.4 * ("Age" / (SELECT MAX("Age") FROM customer_segmentation)) + 
           0.3 * (1 - ("Annual Income (k$)" / (SELECT MAX("Annual Income (k$)") FROM customer_segmentation))) +
           0.3 * (1 - ("Spending Score (1-100)" / 100))), 2) AS total_risiko
	FROM customer_segmentation
);

-- Query untuk melihat total resiko per kategori 
SELECT * FROM Resiko;

-- menentukan diskon terbaik 
CREATE VIEW diskon AS (
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
        (0.2 * (1 - ("Annual Income (k$)" / (SELECT MAX("Annual Income (k$)") FROM customer_segmentation)))) + 
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
        (0.2 * (1 - ("Annual Income (k$)" / (SELECT MAX("Annual Income (k$)") FROM customer_segmentation)))) + 
        (0.2 * (1 - ("Spending Score (1-100)" / 100)))
    ), 2) AS diskon
FROM customer_segmentation
);

SELECT * FROM diskon;

-- buat query untuk perhitungan segmentasi diskon pelanggan 
-- Membuat Segmentasi Diskon Pelanggan
CREATE VIEW segmentasi_diskon AS (
SELECT 
    "CustomerID",
	"Gender",
	"Age",
	"Annual Income (k$)", 
	"Spending Score (1-100)", 
	"kategori_usia",
    -- Klasifikasi Pendapatan
    CASE 
        WHEN "Annual Income (k$)" <= 20000 THEN 'Low Income'
        WHEN "Annual Income (k$)" BETWEEN 20001 AND 60000 THEN 'Middle Income'
        ELSE 'High Income'
    END AS income_group,
    -- Penentuan Tingkat Diskon
    CASE 
        WHEN "Spending Score (1-100)"< 30 THEN 'High Discount (30%)'
        WHEN "Spending Score (1-100)" BETWEEN 30 AND 70 THEN 'Medium Discount (20%)'
        ELSE 'Low Discount (10%)'
    END AS discount_level
FROM customer_segmentation 
ORDER BY "kategori_usia", "income_group", "discount_level"
);

SELECT * FROM segmentasi_diskon;






	
