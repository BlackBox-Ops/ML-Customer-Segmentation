# Dokumentasi Konteks Customer Segmentation System

## 1. Judul dan Deskripsi Sistem
**Judul:** Customer Segmentation System  
**Deskripsi:**  
Sistem ini digunakan untuk membantu admin, analis, dan pengguna akhir dalam mengelola data pelanggan, membuat segmentasi pelanggan, menghasilkan laporan, dan mengatur pengaturan aplikasi dengan otentikasi berbasis peran.

---

## 2. Aktor
| **Aktor**     | **Peran dan Tugas**                                                                 |
|---------------|-------------------------------------------------------------------------------------|
| **Admin**     | Mengelola pengaturan aplikasi, data pelanggan, dan ekspor data.                    |
| **Analyst**   | Mengelola data analitik, menghasilkan laporan, dan menganalisis segmentasi.        |
| **End User**  | Mengakses hasil prediksi, visualisasi segmentasi, dan laporan yang relevan.        |

---

## 3. Deskripsi Use Case
| **Use Case**                      | **Deskripsi**                                                                                     |
|-----------------------------------|-------------------------------------------------------------------------------------------------|
| **Login**                         | Semua aktor harus login untuk mengakses fitur sistem.                                            |
| **Manage and Update Settings**    | Admin dapat memperbarui pengaturan sistem.                                                      |
| **Manage Customer Data**          | Admin mengelola data pelanggan (CRUD operasi).                                                  |
| **Export Data**                   | Admin dapat mengekspor data pelanggan dalam format tertentu.                                     |
| **Data Management**               | Analyst mengelola data untuk analisis lebih lanjut.                                              |
| **Customer Segmentation**         | End User dan Analyst membuat atau menganalisis segmentasi pelanggan.                            |
| **Generate Reports**              | Analyst menghasilkan laporan terkait segmentasi atau hasil analisis lainnya.                   |
| **Predict Customer Segment**      | Sistem memprediksi segmen pelanggan berdasarkan data (*Extend Customer Segmentation*).          |
| **Visualize Customer Segmentation** | Sistem memvisualisasikan segmentasi pelanggan untuk membantu pengguna memahami data.            |

---

## 4. Hubungan Antar Use Case
- Semua *use case* utama memiliki dependensi pada *Login* melalui hubungan `<<include>>`.
- *Customer Segmentation* mencakup prediksi (`<<extend>>`) dan visualisasi segmentasi (`<<extend>>`).
- *Generate Reports* juga terhubung ke *Customer Segmentation* melalui `<<include>>`.

---

## 5. Tabel Relasi Alur Menuju Class Diagram

| **Use Case**                      | **Class**                      | **Relasi**                                                                                       |
|-----------------------------------|--------------------------------|-------------------------------------------------------------------------------------------------|
| **Login**                         | `User`                         | Hubungan antara *User* dan sistem autentikasi.                                                  |
| **Manage Customer Data**          | `Customer`                     | Admin berinteraksi langsung dengan *Customer*.                                                 |
| **Export Data**                   | `Customer`                     | Data pelanggan diekspor melalui fungsi dalam kelas *Customer*.                                  |
| **Data Management**               | `Segment`, `Customer`          | Analyst mengelola data pelanggan dan menghubungkannya ke segmen.                                |
| **Generate Reports**              | `Report`, `Segment`            | *Report* dihasilkan berdasarkan analisis *Segment*.                                             |
| **Visualize Customer Segmentation** | `Segment`                     | Visualisasi memanfaatkan atribut dan metode dari *Segment*.                                     |
