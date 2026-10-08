# 🤖 Sistem Cerdas — Logika Fuzzy (FIS Mamdani)
### MKPT 501 · Modul 2 · Praktikum Sistem Cerdas

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat&logo=python&logoColor=white)
![scikit-fuzzy](https://img.shields.io/badge/scikit--fuzzy-0.4.2-orange?style=flat)
![NumPy](https://img.shields.io/badge/NumPy-1.x-013243?style=flat&logo=numpy)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.x-11557C?style=flat)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-informational?style=flat)
![License](https://img.shields.io/badge/License-Academic-green?style=flat)

---

## 📋 Deskripsi

Repository ini berisi implementasi **Fuzzy Inference System (FIS) Mamdani** menggunakan Python dalam berbagai skenario aplikasi rekayasa kecerdasan buatan, mulai dari perbandingan membership function, estimasi bonus restoran, perencanaan produksi manufaktur, sistem otomasi penyiraman tanaman, hingga sistem kendali kecepatan motor DC.

Program dikembangkan sebagai bagian dari praktikum mata kuliah **MKPT 501 — Sistem Cerdas**, yang bertujuan untuk memahami konsep dasar logika fuzzy secara teori matematis maupun implementasi kode interaktif.

Seluruh program mengikuti alur standar **8 Tahap FIS Mamdani**:

```
Crisp Input → Fuzzifikasi → Evaluasi Rule → Implikasi → Agregasi → Defuzzifikasi → Crisp Output
```

---

## 📁 Struktur File

```
📦 2. Program/
├── 📄 fuzzy_membership.py     # Program 1: Eksplorasi & perbandingan fungsi keanggotaan
├── 📄 fuzzy_bonus.py          # Program 2: FIS untuk menghitung bonus restoran
├── 📄 fuzzy_produksi.py       # Program 3: FIS untuk penentuan jumlah produksi
├── 📄 fuzzy_penyiraman.py     # Program 4: FIS Sistem Penyiraman Tanaman Otomatis (CLI)
├── 📄 fuzzy_penyiraman_gui.py # Program 5: GUI Interaktif FIS Penyiraman (Tkinter + Matplotlib)
├── 📄 fuzzy_motor.py          # Program 6: GUI Interaktif FIS Kendali Kecepatan Motor DC
├── 📄 test_library.py         # Pengujian ketersediaan library Python
├── 📁 hasil/                  # Output grafik (.PNG) yang diekspor dari program
└── 📄 README.md               # Dokumentasi lengkap proyek
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
- 🖨️ Tabel nilai derajat keanggotaan ($\mu$) untuk input uji $x \in \{3, 4, 6, 7\}$

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

---

## 📌 Program 4 & 5 — `fuzzy_penyiraman.py` & `fuzzy_penyiraman_gui.py`
### Sistem Fuzzy Penyiraman Tanaman Otomatis (CLI & GUI Interaktif)

**Tujuan:** Menentukan durasi penyiraman tanaman (dalam menit) berdasarkan variabel masukan **Suhu Udara** dan **Kelembapan Tanah** menggunakan metode inferensi Mamdani.

**Variabel Masukan & Keluaran:**

| Tipe | Variabel | Semesta | Kategori | Parameter MF (`trimf`) |
|------|----------|---------|----------|------------------------|
| **Input** | Suhu Udara | 15 – 40 °C | DINGIN | `[15, 15, 25]` |
| | | | NORMAL | `[20, 27.5, 35]` |
| | | | PANAS | `[30, 40, 40]` |
| **Input** | Kelembapan Tanah | 0 – 100 % | KERING | `[0, 0, 50]` |
| | | | LEMBAP | `[25, 50, 75]` |
| | | | BASAH | `[50, 100, 100]` |
| **Output** | Durasi Penyiraman | 0 – 30 menit | SINGKAT | `[0, 0, 12]` |
| | | | SEDANG | `[8, 15, 22]` |
| | | | LAMA | `[18, 30, 30]` |

**Basis Aturan (9 Rules):**

| No | Suhu | Kelembapan | Durasi |
|----|------|------------|--------|
| R1 | DINGIN | KERING | SEDANG |
| R2 | DINGIN | LEMBAP | SINGKAT |
| R3 | DINGIN | BASAH | SINGKAT |
| R4 | NORMAL | KERING | LAMA |
| R5 | NORMAL | LEMBAP | SEDANG |
| R6 | NORMAL | BASAH | SINGKAT |
| R7 | PANAS | KERING | LAMA |
| R8 | PANAS | LEMBAP | LAMA |
| R9 | PANAS | BASAH | SEDANG |

**Fitur Unggulan Versi GUI (`fuzzy_penyiraman_gui.py`):**
- 🎛️ **Dua Metode Input Tersinkronisasi**: Slider interaktif (respons *real-time*) + Input Manual via keyboard (*Entry* teks).
- 🖱️ **Panel Kontrol Scrollable**: Seluruh 9 aturan *firing strength* ($\alpha$) dan tabel data uji dapat di-scroll lancar menggunakan roda mouse atau scrollbar vertikal.
- 📊 **Visualisasi 4 Tab Terintegrasi**: *Membership Functions*, *Implikasi 9 Aturan*, *Agregasi MAX & Defuzzifikasi Centroid*, serta *Rule Viewer Bar Chart*.
- 💾 **Simpan Gambar Custom via File Explorer**:
  - Tombol simpan per tab (bebas pilih folder dan nama file).
  - Tombol simpan **Semua Bagian (Pisah Tiap File `.png`)** langsung ke folder pilihan pengguna dengan memori posisi folder terakhir (*directory persistence*).
- 📋 **Tabel 10 Data Uji Interaktif**: Klik baris tabel untuk langsung mensimulasikan nilai ke grafik.

**Cara menjalankan:**
```bash
python fuzzy_penyiraman_gui.py
```

---

## 📌 Program 6 — `fuzzy_motor.py`
### Sistem Pengendali Kecepatan Motor DC (GUI Interaktif & Pre-Computation)

**Tujuan:** Mengatur sinyal kendali **PWM (Pulse Width Modulation)** untuk kecepatan motor DC secara adaptif dan presisi berdasarkan kondisi **Error Kecepatan** ($e = SP - PV$) dan laju perubahan error atau **Delta Error** ($\Delta e = \frac{de}{dt}$).

**Variabel Masukan & Keluaran:**

| Tipe | Variabel | Semesta | Kategori | Parameter MF (`trimf`) |
|------|----------|---------|----------|------------------------|
| **Input** | Error ($e$) | -100 s.d. 100 rpm | Negatif | `[-100, -100, 0]` |
| | | | Nol | `[-50, 0, 50]` |
| | | | Positif | `[0, 100, 100]` |
| **Input** | Delta Error ($\Delta e$) | -20 s.d. 20 rpm/siklus | Negatif | `[-20, -20, 0]` |
| | | | Nol | `[-10, 0, 10]` |
| | | | Positif | `[0, 20, 20]` |
| **Output** | Sinyal PWM Motor | 0 – 255 (8-bit) | Rendah | `[0, 0, 128]` |
| | | | Sedang | `[64, 128, 192]` |
| | | | Tinggi | `[128, 255, 255]` |

**Basis Aturan (Rule Base) — 9 Rule IF-THEN:**

| Rule | Kondisi Error ($e$) | Kondisi Delta Error ($\Delta e$) | Tindakan Sinyal PWM | Interpretasi Fisik |
|:----:|:-------------------:|:-------------------------------:|:-------------------:|:-------------------|
| **R1** | Negatif | Negatif | **Rendah** | Motor berputar melebihi setpoint dan makin cepat → kurangi daya PWM secara drastis |
| **R2** | Negatif | Nol | **Rendah** | Motor terlalu cepat namun stabil → turunkan kecepatan |
| **R3** | Negatif | Positif | **Sedang** | Motor terlalu cepat tapi mulai melambat → pertahankan daya sedang |
| **R4** | Nol | Negatif | **Rendah** | Kecepatan pas pada setpoint tapi ada akselerasi naik → turunkan sedikit daya |
| **R5** | Nol | Nol | **Sedang** | Kecepatan stabil tepat di setpoint → pertahankan kondisi steady-state |
| **R6** | Nol | Positif | **Tinggi** | Kecepatan pas tapi mulai drop → suntikkan daya tambahan |
| **R7** | Positif | Negatif | **Sedang** | Motor kurang cepat tapi laju mulai naik mendekati setpoint → daya sedang |
| **R8** | Positif | Nol | **Tinggi** | Motor kurang cepat dan diam di tempat → naikkan daya ke level tinggi |
| **R9** | Positif | Positif | **Tinggi** | Motor lambat dan makin tertinggal jauh → berikan daya maksimal |

**Fitur Unggulan Program & GUI:**
- 🖨️ **Pre-Run Benchmark Terminal (Otomatis)**:  
  Sebelum jendela GUI ditampilkan ke layar, fungsi `jalankan_pengujian_terminal()` secara otomatis menghitung dan mencetak tabel evaluasi lengkap dari 10 skenario eksperimen `(Error, Delta Error)` ke konsol.
- 🎛️ **Slider Taktil 3D Elegan**:  
  Slider dirancang menggunakan style khusus `Motor.Horizontal.TScale` berbasis tema Clam dengan knob timbul bertekstur (*raised 3D*), aksen biru modern (`#378ADD`), border kontras, dan cursor tangan interaktif yang nyaman digeser.
- 🔄 **Sinkronisasi Input Ganda**:  
  Nilai dapat diatur lewat slider interaktif atau langsung diketik pada kotak isian *Entry* secara *real-time* dua arah.
- 📊 **Visualisasi Grafis 1 Halaman Utuh (Multi-Plot Canvas)**:
  - Grafik fungsi keanggotaan Error, Delta Error, dan PWM beserta garis vertikal penunjuk nilai input aktif.
  - Subplot implikasi individual untuk 9 aturan lengkap dengan nilai *firing strength* ($\alpha$).
  - Kurva Agregasi MAX dan garis defuzzifikasi Centroid titik berat.
  - Grafik batang horizontal *Rule Viewer* untuk memantau kontribusi tiap aturan.
- 💾 **Simpan Gambar Satu Halaman Penuh via File Explorer**:
  - Tombol simpan ganda pada panel kontrol kiri dan di bawah canvas visualisasi.
  - Terintegrasi langsung dengan `filedialog.asksaveasfilename` yang mengingat direktori folder terakhir yang dipilih (*directory persistence*).
  - Grafik disimpan dalam resolusi tinggi (DPI 120) tanpa bagian yang terpotong.
- ⚡ **Kartu Metrik & Status Real-time**: Menampilkan nilai PWM (0–255), persentase *Duty Cycle* (%), serta badge kategori kecepatan dinamis (Rendah / Sedang / Tinggi).

**Tabel Hasil Pengujian 10 Skenario Percobaan:**

| No | Error (rpm) | Delta Error (rpm/s) | Nilai PWM (0–255) | Duty Cycle (%) | Kategori Output |
|:--:|:-----------:|:-------------------:|:-----------------:|:--------------:|:---------------:|
| 1  | -80         | -15                 | 44.80             | 17.57 %        | Rendah          |
| 2  | -40         | 0                   | 77.29             | 30.31 %        | Rendah          |
| 3  | -30         | 10                  | 170.73            | 66.95 %        | Sedang          |
| 4  | -5          | -5                  | 102.95            | 40.37 %        | Sedang          |
| 5  | 0           | 0                   | 128.00            | 50.20 %        | Sedang          |
| 6  | 10          | 5                   | 152.66            | 59.87 %        | Sedang          |
| 7  | 30          | -10                 | 84.74             | 33.23 %        | Rendah          |
| 8  | 50          | 10                  | 205.61            | 80.63 %        | Tinggi          |
| 9  | 80          | 15                  | 210.55            | 82.57 %        | Tinggi          |
| 10 | 100         | 20                  | 212.67            | 83.40 %        | Tinggi          |

**Cara menjalankan:**
```bash
python fuzzy_motor.py
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

Program dalam repositori ini mengimplementasikan **FIS Mamdani** melalui alur 8 tahap:

```
┌─────────────────────────────────────────────────────────────────┐
│                    ALUR FIS MAMDANI                             │
├───────┬─────────────────────────────────────────────────────────┤
│ Tahap │ Deskripsi                                               │
├───────┼─────────────────────────────────────────────────────────┤
│   1   │ Definisi Fungsi Keanggotaan (trimf / segitiga)          │
│   2   │ Fuzzifikasi Input → hitung μ(x) tiap kategori           │
│   3   │ Evaluasi Rule dengan operator AND = MIN                 │
│   4   │ Hitung Firing Strength (α) tiap rule                    │
│   5   │ Implikasi MIN → potong kurva output sesuai α            │
│   6   │ Agregasi MAX → gabungkan semua kurva implikasi          │
│   7   │ Defuzzifikasi Centroid → hasilkan nilai crisp output    │
│   8   │ Visualisasi Rule Viewer & Analisis Hasil                │
└───────┴─────────────────────────────────────────────────────────┘
```

**Metode yang digunakan:**
- Fungsi Keanggotaan : **Triangular (`trimf`)**
- Operator AND       : **Minimum (`np.fmin`)**
- Implikasi          : **Minimum (`np.fmin`)**
- Agregasi           : **Maximum (`np.fmax`)**
- Defuzzifikasi      : **Centroid / Center of Gravity (`fuzz.defuzz`)**

---

## 📚 Library yang Digunakan

| Library | Versi | Fungsi |
|---------|-------|--------|
| `numpy` | ≥ 1.21 | Operasi array numerik multidimensi dan fungsi matematika |
| `scikit-fuzzy` | ≥ 0.4 | Fungsi keanggotaan fuzzy, interpolasi, dan defuzzifikasi |
| `matplotlib` | ≥ 3.4 | Rendering visualisasi grafik teknis dan multi-subplot canvas |
| `tkinter` | Bawaan Python | Antarmuka grafis desktop interaktif (GUI) |

---

## 👤 Informasi
> **Nama :** Teuku Azhar Pasha <br /> 
> **NIM :** 202406036 <br />
> **Dosen Pengampu :** Dr. Emmanuel Agung Nughroho S.T., M.T. <br/>
> **Mata Kuliah :** MKPT 501 — Sistem Cerdas  
> **Program :** PEI Semester 5  
> **Modul :** M2 — Logika Fuzzy (FIS Mamdani)  
> **Tanggal :** 08 Oktober 2026
