# Seporsi Ayam Goreng, Berapa Menit Kerja?

Kalkulator personal **Indeks Ayam Goreng**: masukkan kota dan gajimu, lalu lihat berapa menit kerja yang dibutuhkan untuk membeli seporsi ayam goreng di 34 ibu kota provinsi. Terinspirasi dari [Indeks Ayam Goreng Kompas](https://www.kompas.id/artikel/ayam-goreng-kupang-tiga-kali-lebih-mahal-dari-jakarta-hl1).

## Struktur

```
index.html                          aplikasi (memuat data lewat fetch)
data/ayam-goreng-34-kota-2025.json  data yang dipakai aplikasi
data/ayam-goreng-34-kota-2025.csv   data yang sama dalam CSV
vendor/                             Chart.js, plugin datalabels, CSS/JS desain
scripts/build_inline.py             membuat dist/index.html satu file (data ditanam)
```

## Menjalankan

Karena data dimuat dengan `fetch`, buka lewat server web, bukan `file://`:

```bash
python3 -m http.server 8000
# buka http://localhost:8000
```

Untuk versi satu file (offline atau platform yang memblokir file terpisah):

```bash
python3 scripts/build_inline.py   # hasil: dist/index.html
```

## Metode

- Harga: rata-rata harga ayam goreng per porsi di ibu kota provinsi, BPS 2025 (Tabel 78).
- Rumus: `menit = harga / (gaji / 9.600)`. Asumsi 40 jam/minggu = 9.600 menit/bulan, sama dengan Kompas.
- Hasil dibulatkan ke menit terdekat (0,5 ke atas), mengikuti angka di artikel Kompas.
- Pembanding: upah minimum 2025 (UMK; Jakarta, Jayapura, Pangkal Pinang, Manokwari, dan Gorontalo memakai UMP karena tidak menetapkan UMK).
- Gaji dihitung kotor. Perhitungan berjalan di perangkat pengguna; gaji tidak dikirim atau disimpan.

## Kolom data

`kota`, `nama_bps`, `harga_ayam_goreng_2025_rp_porsi`, `menit_kerja_umk_2023/2024/2025` (angka Kompas), `umk_2025_tersirat_rp`, `upah_minimum_2025_rp`, `jenis_upah_minimum`, `sumber_upah_minimum`, `menit_kerja_hitung_ulang_2025` (dibulatkan 1 desimal, hanya untuk referensi; aplikasi menghitung ulang dari data mentah).

Dibuat oleh [Haris Firdaus](https://haris.ai.id).
