# Analisis Data Sintesis Operasional Penjualan

## 1. Tujuan

Analisis ini menggunakan 1.000 observasi sintetis yang dibangun dari dua data awal pada Bedah Kasus 1. Tujuannya adalah menyediakan data latihan yang cukup untuk statistik deskriptif, visualisasi variabel kategorik, numerik, dan waktu, serta dashboard interaktif.

## 2. Batasan data

Data awal hanya terdiri dari dua observasi:

| Produk | Kategori | Harga | Jumlah Terjual | Tanggal |
|---|---|---:|---:|---|
| Laptop | Elektronik | Rp8.500.000 | 45 | 01/01/2024 |
| Buku | Pendidikan | Rp75.000 | 120 | 02/01/2024 |

Dua observasi tersebut tidak cukup untuk mengestimasi distribusi populasi secara empiris. Karena itu, data 1.000 baris harus diperlakukan sebagai **data sintesis**, bukan data historis.

## 3. Desain sintesis

- Seed acak: **42**, sehingga hasil dapat direplikasi.
- Jumlah observasi: **1.000**.
- Periode: **1 Januari 2024 sampai 31 Desember 2024**.
- Produk: Laptop dan Buku.
- Kategori: Elektronik dan Pendidikan.
- Harga: variasi normal terbatas di sekitar harga acuan.
- Jumlah terjual: distribusi Poisson dengan rata-rata yang mengikuti produk.
- Variasi waktu: faktor bulanan dan akhir pekan.
- Omzet: `Harga_Rp × Jumlah_Terjual`.

## 4. Statistik utama

- Total observasi: **1,000**
- Total unit terjual: **82,996**
- Total omzet: **Rp 197,400,417,000**
- Rata-rata jumlah terjual per observasi: **83.00 unit**
- Median jumlah terjual: **66 unit**
- Harga rata-rata: **Rp 4,277,614**
- Jumlah terjual minimum-maksimum: **22 sampai 169 unit**

## 5. Analisis produk

### Laptop

Laptop memiliki 503 observasi. Total penjualan mencapai 22,880 unit. Omzet mencapai **Rp 192,890,745,000**. Kontribusi omzet Laptop sebesar **97.72%** dari total omzet.

### Buku

Buku memiliki 497 observasi. Total penjualan mencapai 60,116 unit. Omzet mencapai **Rp 4,509,672,000**. Kontribusi omzet Buku sebesar **2.28%** dari total omzet.

Temuan utama: Buku menghasilkan volume unit jauh lebih tinggi, tetapi Laptop mendominasi omzet karena harga per unit jauh lebih besar.

## 6. Analisis waktu

Bulan dengan omzet tertinggi adalah **2024-04**, dengan omzet sekitar **Rp 21,041,376,000**.

Bulan dengan jumlah unit terjual tertinggi adalah **2024-12**, dengan total **8,941 unit**.

Perbedaan antara bulan dengan omzet tertinggi dan volume tertinggi menunjukkan bahwa omzet tidak hanya dipengaruhi jumlah unit. Komposisi produk dan harga juga menentukan nilai penjualan.

## 7. Analisis hubungan variabel

Korelasi Harga dan Jumlah Terjual pada data sintesis adalah **-0.952**. Nilai ini kuat dan negatif. Namun, hasil tersebut tidak boleh langsung ditafsirkan sebagai hukum bahwa kenaikan harga menyebabkan penurunan penjualan.

Penyebab utamanya adalah struktur data sintesis. Laptop memiliki harga jutaan rupiah dan jumlah terjual lebih rendah. Buku memiliki harga puluhan ribu rupiah dan jumlah terjual lebih tinggi. Perbedaan antarproduk tersebut dapat menghasilkan korelasi agregat yang tinggi.

Untuk penelitian yang lebih kuat, analisis hubungan harga dan jumlah terjual perlu dilakukan dengan data transaksi nyata dan, jika diperlukan, model regresi yang mengontrol produk, kategori, periode, promosi, dan faktor lain.

## 8. Implikasi visualisasi

Struktur variabel pada kasus ini mendukung beberapa bentuk visualisasi:

1. **Bar chart** untuk membandingkan omzet atau unit menurut Produk dan Kategori.
2. **Pie chart** untuk melihat komposisi kontribusi jika jumlah kategori sedikit.
3. **Histogram** untuk memeriksa distribusi Harga dan Jumlah Terjual.
4. **Scatter plot** untuk melihat hubungan Harga dan Jumlah Terjual.
5. **Line chart** untuk melihat tren omzet dan unit dari waktu ke waktu.

Dashboard Streamlit pada project ini menggabungkan visualisasi tersebut dengan filter tanggal, produk, dan kategori.
