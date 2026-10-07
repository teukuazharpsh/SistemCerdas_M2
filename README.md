# 🤖 Sistem Cerdas — Logika Fuzzy (FIS Mamdani)
### MKPT 501 · Modul 2 · Praktikum Sistem Cerdas

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat&logo=python&logoColor=white)
![scikit-fuzzy](https://img.shields.io/badge/scikit--fuzzy-0.4.2-orange?style=flat)
![NumPy](https://img.shields.io/badge/NumPy-1.x-013243?style=flat&logo=numpy)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.x-11557C?style=flat)
![License](https://img.shields.io/badge/License-Academic-green?style=flat)

---

## 📋 Deskripsi

Repository ini berisi implementasi **Fuzzy Inference System (FIS) Mamdani** menggunakan Python dalam tiga skenario berbeda.  
Program dikembangkan sebagai bagian dari praktikum mata kuliah **MKPT 501 — Sistem Cerdas**, yang bertujuan untuk memahami konsep dasar logika fuzzy secara teori maupun implementasi kode.

Seluruh program mengikuti alur standar **8 Tahap FIS Mamdani**:

```
Crisp Input → Fuzzifikasi → Evaluasi Rule → Implikasi → Agregasi → Defuzzifikasi → Crisp Output
```

---

## 📁 Struktur File

```
📦 2. Program/
├── 📄 fuzzy_membership.py    # Program 1: Eksplorasi & perbandingan fungsi keanggotaan
├── 📄 fuzzy_bonus.py         # Program 2: FIS untuk menghitung bonus restoran
├── 📄 fuzzy_produksi.py      # Program 3: FIS untuk penentuan jumlah produksi
├── 📄 test_library.py        # Pengujian ketersediaan library
├── 📁 hasil/                 # Output grafik (PNG) yang dihasilkan program
└── 📄 README.md
```

---

## 📌 Program 1 — `fuzzy_membership.py`
### Eksplorasi Fungsi Keanggotaan Pelayanan

**Tujuan:** Memvisualisasikan dan membandingkan dua variasi kurva fungsi keanggotaan segitiga (*triangular membership function*) untuk variabel **Pelayanan**, serta melakukan fuzzifikasi manual pada nilai-nilai uji.

**Variabel:**

| Variabel | Semesta | Kategori |
|----------|---------|----------|
| Pelayanan | 0 – 10 | MENGECEWAKAN · BAGUS · MEMUASKAN |

**Variasi yang dibandingkan:**

| Variasi | Parameter Kurva BAGUS |
|---------|----------------------|
| Awal | `[2.5, 5, 7.5]` (simetris) |
| Modifikasi | `[3, 5, 8]` (asimetris ke kanan) |

**Output yang dihasilkan:**
- 📊 Grafik perbandingan 2 variasi fungsi keanggotaan → `hasil/p1_membership.png`
- 🖨️ Tabel nilai derajat keanggotaan (μ) untuk input uji `x = {3, 4, 6, 7}`

**Cara menjalankan:**
```bash
python fuzzy_membership.py
```

---

## 📌 Program 2 — `fuzzy_bonus.py`
### FIS Mamdani — Perhitungan Bonus Restoran

**Tujuan:** Menentukan besaran **bonus tip** yang diberikan kepada pelayan restoran berdasarkan kualitas **pelayanan** dan **makanan** menggunakan Fuzzy Inference System Mamdani.

**Variabel Input & Output:**

| Variabel | Semesta | Kategori |
|----------|---------|----------|
| Pelayanan *(input)* | 0 – 10 | MENGECEWAKAN · BAGUS · MEMUASKAN |
| Makanan *(input)* | 0 – 10 | HAMBAR · ENAK |
| Bonus *(output)* | 0 – 30 | SEDIKIT · SEDANG · BANYAK |

**Basis Aturan (Rule Base) — 6 Rule IF-THEN:**

| Rule | Kondisi Pelayanan | Kondisi Makanan | Output Bonus |
|------|:-----------------:|:---------------:|:------------:|
| R1 | MENGECEWAKAN | HAMBAR | **SEDIKIT** |
| R2 | MENGECEWAKAN | ENAK | **SEDIKIT** |
| R3 | BAGUS | HAMBAR | **SEDIKIT** |
| R4 | BAGUS | ENAK | **SEDANG** |
| R5 | MEMUASKAN | HAMBAR | **SEDANG** |
| R6 | MEMUASKAN | ENAK | **BANYAK** |

**Output yang dihasilkan:**
- 📊 Grafik fungsi keanggotaan + garis input → `hasil/p2_membership.png`
- 📊 Grafik implikasi, agregasi, dan centroid → `hasil/p2_agregasi.png`
- 📊 Grafik batang Rule Viewer → `hasil/p2_ruleviewer.png`
- 🖨️ Nilai fuzzifikasi dan hasil bonus crisp di terminal

**Cara menjalankan:**
```bash
python fuzzy_bonus.py
```
```
Nilai pelayanan (0-10): 7
Nilai makanan   (0-10): 8
```

---

## 📌 Program 3 — `fuzzy_produksi.py`
### FIS Mamdani — Penentuan Jumlah Produksi

**Tujuan:** Menentukan jumlah **target produksi kemasan per hari** berdasarkan tingkat **permintaan pasar** dan **persediaan stok** di gudang menggunakan Fuzzy Inference System Mamdani, beserta pengujian batch 10 skenario data.

**Variabel Input & Output:**

| Variabel | Semesta | Kategori |
|----------|---------|----------|
| Permintaan *(input)* | 1000 – 5000 unit | TURUN · TETAP · NAIK |
| Persediaan *(input)* | 100 – 600 unit | SEDIKIT · SEDANG · BANYAK |
| Produksi *(output)* | 2000 – 7000 kemasan/hari | BERKURANG · TETAP · BERTAMBAH |

**Basis Aturan (Rule Base) — 9 Rule IF-THEN:**

| Rule | Permintaan | Persediaan | Produksi |
|------|:----------:|:----------:|:--------:|
| R1 | TURUN | SEDIKIT | **BERKURANG** |
| R2 | TURUN | SEDANG | **BERKURANG** |
| R3 | TURUN | BANYAK | **BERKURANG** |
| R4 | TETAP | SEDIKIT | **BERTAMBAH** |
| R5 | TETAP | SEDANG | **TETAP** |
| R6 | TETAP | BANYAK | **BERKURANG** |
| R7 | NAIK | SEDIKIT | **BERTAMBAH** |
| R8 | NAIK | SEDANG | **BERTAMBAH** |
| R9 | NAIK | BANYAK | **BERTAMBAH** |

**Output yang dihasilkan:**
- 📊 Grafik fungsi keanggotaan + garis input → `hasil/p3_membership.png`
- 📊 Grid grafik implikasi 9 rule → `hasil/p3_implikasi.png`
- 📊 Grafik agregasi dan defuzzifikasi → `hasil/p3_agregasi.png`
- 📊 Grafik batang Rule Viewer → `hasil/p3_ruleviewer.png`
- 🖨️ Tabel hasil pengujian 10 skenario data di terminal

**Cara menjalankan:**
```bash
python fuzzy_produksi.py
```
```
Permintaan (1000-5000): 3800
Persediaan (100-600)  : 250
```

**Contoh output tabel 10 data uji:**
```
No | Permintaan | Persediaan | Produksi
 1 |       1000 |        100 |  2833.33
 2 |       1500 |        500 |  2928.57
 3 |       2000 |        200 |  2972.22
 ...
10 |       3800 |        250 |  5590.36
```

---

## ⚙️ Instalasi & Persyaratan

### Prasyarat
- Python **3.10** atau lebih baru
- pip (package installer Python)

### Instalasi Library

```bash
pip install numpy scikit-fuzzy matplotlib
```

Atau verifikasi library sudah terinstall dengan menjalankan:
```bash
python test_library.py
```
```
Numpy berhasil
Sckitt fuzzy berhasil
Matploit berhasil
```

---

## 🧠 Konsep Dasar Logika Fuzzy

Program ini mengimplementasikan **FIS Mamdani** melalui alur berikut:

```
┌─────────────────────────────────────────────────────────────────┐
│                    ALUR FIS MAMDANI                             │
├───────┬─────────────────────────────────────────────────────────┤
│ Tahap │ Deskripsi                                               │
├───────┼─────────────────────────────────────────────────────────┤
│   1   │ Definisi Fungsi Keanggotaan (trimf / segitiga)          │
│   2   │ Fuzzifikasi Input → hitung μ(x) tiap kategori           │
│   3   │ Evaluasi Rule dengan operator AND = MIN                  │
│   4   │ Hitung Firing Strength (α) tiap rule                    │
│   5   │ Implikasi MIN → potong kurva output sesuai α            │
│   6   │ Agregasi MAX → gabungkan semua kurva implikasi          │
│   7   │ Defuzzifikasi Centroid → hasilkan nilai crisp output    │
│   8   │ Visualisasi Rule Viewer                                  │
└───────┴─────────────────────────────────────────────────────────┘
```

**Metode yang digunakan:**
- Fungsi Keanggotaan : **Triangular (trimf)**
- Operator AND       : **Minimum (fmin)**
- Implikasi         : **Minimum (fmin)**
- Agregasi          : **Maximum (fmax)**
- Defuzzifikasi     : **Centroid (Center of Gravity)**

---

## 📚 Library yang Digunakan

| Library | Versi | Fungsi |
|---------|-------|--------|
| `numpy` | ≥ 1.21 | Array numerik dan operasi matematika |
| `scikit-fuzzy` | ≥ 0.4 | Fungsi keanggotaan, interpolasi, defuzzifikasi |
| `matplotlib` | ≥ 3.4 | Visualisasi grafik dan plot |

---

## 👤 Informasi
> **Nama :** Teuku Azhar Pasha >
> **NIM :** 202406036
> **Mata Kuliah :** MKPT 501 — Sistem Cerdas  
> **Program :** PEI Semester 5  
> **Modul :** M2 — Logika Fuzzy (FIS Mamdani)  
> **Tanggal :** 07 Oktober 2026
> **Dosen Pengampu :** Dr. Emmanuel Agung Nughroho S.T., M.T.
