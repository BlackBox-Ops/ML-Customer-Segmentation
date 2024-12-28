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

