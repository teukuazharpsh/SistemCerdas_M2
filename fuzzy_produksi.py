# Mengimpor modul os untuk membuat folder, dan sys untuk menghentikan program saat error
import os, sys

# Mengimpor numpy untuk operasi array dan perhitungan numerik
import numpy as np

# Mengimpor scikit-fuzzy untuk fungsi keanggotaan fuzzy dan defuzzifikasi
import skfuzzy as fuzz

# Mengimpor matplotlib untuk membuat grafik visualisasi
import matplotlib.pyplot as plt

# Membuat folder 'hasil' jika belum ada, untuk menyimpan semua output gambar grafik
os.makedirs("hasil", exist_ok=True)

# ──────────────────────────────────────────────────────────────────────────────
# DEFINISI SEMESTA PEMBICARAAN (Universe of Discourse)
# ──────────────────────────────────────────────────────────────────────────────

# Semesta untuk variabel input PERMINTAAN: rentang 1000–5000 unit dengan langkah 1
permintaan = np.arange(1000, 5001, 1)

# Semesta untuk variabel input PERSEDIAAN: rentang 100–600 unit dengan langkah 1
persediaan = np.arange(100, 601, 1)

# Semesta untuk variabel output PRODUKSI: rentang 2000–7000 kemasan/hari dengan langkah 1
produksi   = np.arange(2000, 7001, 1)

# ──────────────────────────────────────────────────────────────────────────────
# DEFINISI FUNGSI KEANGGOTAAN (Membership Functions) — kurva SEGITIGA (trimf)
# ──────────────────────────────────────────────────────────────────────────────

# Fungsi keanggotaan untuk variabel PERMINTAAN (3 kategori):
# - TURUN : kurva segitiga dari [1000, 1000, 3000] → puncak di 1000, turun ke 0 di 3000
# - TETAP : kurva segitiga dari [2000, 3000, 4000] → puncak di 3000 (permintaan stabil)
# - NAIK  : kurva segitiga dari [3000, 5000, 5000] → naik dari 3000, puncak di 5000
mf_permintaan = {"TURUN": fuzz.trimf(permintaan, [1000, 1000, 3000]),
                 "TETAP": fuzz.trimf(permintaan, [2000, 3000, 4000]),
                 "NAIK":  fuzz.trimf(permintaan, [3000, 5000, 5000])}

# Fungsi keanggotaan untuk variabel PERSEDIAAN (3 kategori):
# - SEDIKIT : [100, 100, 350] → stok rendah
# - SEDANG  : [200, 350, 500] → stok menengah
# - BANYAK  : [350, 600, 600] → stok tinggi
mf_persediaan = {"SEDIKIT": fuzz.trimf(persediaan, [100, 100, 350]),
                 "SEDANG":  fuzz.trimf(persediaan, [200, 350, 500]),
                 "BANYAK":  fuzz.trimf(persediaan, [350, 600, 600])}

# Fungsi keanggotaan untuk variabel output PRODUKSI (3 kategori):
# - BERKURANG : [2000, 2000, 4500] → produksi dikurangi
# - TETAP     : [3500, 4500, 5500] → produksi dipertahankan
# - BERTAMBAH : [5000, 7000, 7000] → produksi ditingkatkan
mf_produksi = {"BERKURANG": fuzz.trimf(produksi, [2000, 2000, 4500]),
               "TETAP":     fuzz.trimf(produksi, [3500, 4500, 5500]),
               "BERTAMBAH": fuzz.trimf(produksi, [5000, 7000, 7000])}

# ──────────────────────────────────────────────────────────────────────────────
# DEFINISI RULE BASE (Basis Aturan Fuzzy — 9 Rule IF-THEN)
# Format setiap tuple: (kondisi_permintaan, kondisi_persediaan, output_produksi)
# ──────────────────────────────────────────────────────────────────────────────

RULE = [
    ("TURUN", "SEDIKIT", "BERKURANG"),  # R1: Permintaan turun & stok sedikit → produksi berkurang
    ("TURUN", "SEDANG",  "BERKURANG"),  # R2: Permintaan turun & stok sedang  → produksi berkurang
    ("TURUN", "BANYAK",  "BERKURANG"),  # R3: Permintaan turun & stok banyak  → produksi berkurang
    ("TETAP", "SEDIKIT", "BERTAMBAH"),  # R4: Permintaan tetap & stok sedikit → produksi bertambah
    ("TETAP", "SEDANG",  "TETAP"),      # R5: Permintaan tetap & stok sedang  → produksi tetap
    ("TETAP", "BANYAK",  "BERKURANG"),  # R6: Permintaan tetap & stok banyak  → produksi berkurang
    ("NAIK",  "SEDIKIT", "BERTAMBAH"),  # R7: Permintaan naik  & stok sedikit → produksi bertambah
    ("NAIK",  "SEDANG",  "BERTAMBAH"),  # R8: Permintaan naik  & stok sedang  → produksi bertambah
    ("NAIK",  "BANYAK",  "BERTAMBAH"),  # R9: Permintaan naik  & stok banyak  → produksi bertambah
]

# ──────────────────────────────────────────────────────────────────────────────
# FUNGSI UTAMA: Fuzzy Inference System (FIS) Mamdani
# Menerima nilai crisp input → mengembalikan semua hasil proses FIS
# ──────────────────────────────────────────────────────────────────────────────

def hitung_fis(nilai_permintaan, nilai_persediaan):
    # TAHAP 2 — Fuzzifikasi Permintaan:
    # Menghitung derajat keanggotaan (μ) nilai permintaan untuk setiap kategori (TURUN/TETAP/NAIK)
    mu_p = {k: fuzz.interp_membership(permintaan, f, nilai_permintaan) for k, f in mf_permintaan.items()}

    # TAHAP 3 — Fuzzifikasi Persediaan:
    # Menghitung derajat keanggotaan (μ) nilai persediaan untuk setiap kategori (SEDIKIT/SEDANG/BANYAK)
    mu_s = {k: fuzz.interp_membership(persediaan, f, nilai_persediaan) for k, f in mf_persediaan.items()}

    # TAHAP 4 — Evaluasi Rule (AND = MIN):
    # Menghitung firing strength (alpha) setiap rule dengan mengambil nilai minimum dari dua kondisi
    alpha = [np.fmin(mu_p[a], mu_s[b]) for a, b, _ in RULE]

    # TAHAP 5 — Implikasi (MIN):
    # Memotong kurva output produksi di ketinggian alpha masing-masing rule
    output_rule = [np.fmin(al, mf_produksi[c]) for al, (_, _, c) in zip(alpha, RULE)]

    # TAHAP 6 — Agregasi (MAX):
    # Inisialisasi array hasil agregasi dengan nilai 0 (belum ada kontribusi rule)
    aggregated = np.zeros_like(produksi, dtype=float)

    # Menggabungkan semua kurva implikasi menggunakan operasi MAX (ambil nilai tertinggi tiap titik)
    for o in output_rule:
        aggregated = np.fmax(aggregated, o)

    # TAHAP 7 — Defuzzifikasi (Centroid):
    # Menghitung nilai crisp produksi akhir menggunakan metode pusat massa (centroid)
    hasil = fuzz.defuzz(produksi, aggregated, "centroid")

    # Mengembalikan semua hasil proses FIS untuk digunakan pada visualisasi dan output
    return mu_p, mu_s, alpha, output_rule, aggregated, hasil

# ══════════════════════════════════════════════════════════════════════════════
# INPUT NILAI CRISP dari pengguna
# ══════════════════════════════════════════════════════════════════════════════

# Menerima input nilai permintaan (1000–5000) dan mengonversinya ke float
nilai_permintaan = float(input("Permintaan (1000-5000): "))

# Menerima input nilai persediaan (100–600) dan mengonversinya ke float
nilai_persediaan = float(input("Persediaan (100-600)  : "))

# Validasi input: jika nilai di luar rentang semesta, hentikan program dengan pesan error
if not (1000 <= nilai_permintaan <= 5000 and 100 <= nilai_persediaan <= 600):
    sys.exit("Input di luar semesta pembicaraan.")

# Menjalankan fungsi FIS dan menampung semua hasil ke variabel masing-masing
mu_p, mu_s, alpha, output_rule, aggregated, hasil = hitung_fis(nilai_permintaan, nilai_persediaan)

# ══════════════════════════════════════════════════════════════════════════════
# OUTPUT — Menampilkan hasil perhitungan ke layar
# ══════════════════════════════════════════════════════════════════════════════

# Menampilkan header dan hasil fuzzifikasi untuk setiap kategori PERMINTAAN
print("\n== FUZZIFIKASI PERMINTAAN ==")
for k, v in mu_p.items(): print(f"{k:<8} = {v:.4f}")

# Menampilkan header dan hasil fuzzifikasi untuk setiap kategori PERSEDIAAN
print("\n== FUZZIFIKASI PERSEDIAAN ==")
for k, v in mu_s.items(): print(f"{k:<8} = {v:.4f}")

# Menampilkan header dan firing strength (alpha) setiap rule
print("\n== FIRING STRENGTH ==")
for i, (a, b, c) in enumerate(RULE, 1):
    # Menampilkan detail rule ke-i: kondisi input, output rule, dan nilai alpha-nya
    print(f"R{i}: IF {a} AND {b} THEN {c:<9} -> alpha = {alpha[i-1]:.4f}")

# Menampilkan nilai produksi akhir hasil defuzzifikasi
print(f"\nHASIL PRODUKSI = {hasil:.2f} kemasan/hari")

# ══════════════════════════════════════════════════════════════════════════════
# TAHAP 1: Visualisasi Grafik Fungsi Keanggotaan + Garis Input
# ══════════════════════════════════════════════════════════════════════════════

# Membuat 3 subplot berdampingan (Permintaan | Persediaan | Produksi)
fig, axs = plt.subplots(1, 3, figsize=(16, 4.5))

# Melakukan perulangan untuk menggambar kurva MF pada masing-masing subplot
for ax, (x, mf, judul, nilai) in zip(axs, [
        # Subplot 1: MF Permintaan dengan garis input
        (permintaan, mf_permintaan, "Permintaan", nilai_permintaan),
        # Subplot 2: MF Persediaan dengan garis input
        (persediaan, mf_persediaan, "Persediaan", nilai_persediaan),
        # Subplot 3: MF Produksi (output, tidak ada garis input)
        (produksi,   mf_produksi,   "Produksi",   None)]):

    # Menggambar setiap kurva fungsi keanggotaan
    for nama, f in mf.items():
        ax.plot(x, f, label=nama)

    # Jika ada nilai input, gambar garis vertikal penanda posisi input crisp
    if nilai is not None:
        ax.axvline(nilai, color="k", linestyle="--", label=f"Input = {nilai:g}")

    # Mengatur judul, label sumbu, grid, dan legenda setiap subplot
    ax.set_title(f"Membership Function {judul}")
    ax.set_xlabel(judul); ax.set_ylabel("Derajat Keanggotaan"); ax.grid(); ax.legend()

# Merapikan tata letak, menyimpan gambar, dan menampilkan grafik
plt.tight_layout(); plt.savefig("hasil/p3_membership.png", dpi=150); plt.show()

# ══════════════════════════════════════════════════════════════════════════════
# TAHAP 5: Visualisasi Hasil Implikasi (MIN) Setiap Rule
# ══════════════════════════════════════════════════════════════════════════════

# Membuat grid grafik 3x3 (satu panel per rule) dengan sumbu X dan Y yang sama
fig, axs = plt.subplots(3, 3, figsize=(14, 9), sharex=True, sharey=True)

# Melakukan perulangan untuk setiap rule dan panel grafik
for i, ax in enumerate(axs.ravel()):
    # Menggambar area kurva output rule ke-i yang sudah dipotong pada ketinggian alpha
    ax.fill_between(produksi, output_rule[i], alpha=0.4)
    # Mengatur judul panel dengan nomor rule dan nilai alpha-nya
    ax.set_title(f"R{i+1} (alpha = {alpha[i]:.2f})"); ax.grid()

# Mengatur judul utama untuk seluruh figure
fig.suptitle("Implikasi (MIN) setiap rule")

# Merapikan tata letak, menyimpan gambar, dan menampilkan grafik implikasi
plt.tight_layout(); plt.savefig("hasil/p3_implikasi.png", dpi=150); plt.show()

# ══════════════════════════════════════════════════════════════════════════════
# TAHAP 6–7: Visualisasi Agregasi (MAX) dan Defuzzifikasi (Centroid)
# ══════════════════════════════════════════════════════════════════════════════

# Membuat grafik baru berukuran 9x4.5 inci
plt.figure(figsize=(9, 4.5))

# Menggambar area agregasi (gabungan semua kurva implikasi) dengan transparansi 0.4
plt.fill_between(produksi, aggregated, alpha=0.4, label="Agregasi (MAX)")

# Menggambar garis vertikal merah penanda nilai centroid (hasil defuzzifikasi)
plt.axvline(hasil, color="r", linestyle="--", label=f"Centroid = {hasil:.2f}")

# Mengatur judul dan label sumbu grafik agregasi
plt.title("Agregasi dan Defuzzifikasi"); plt.xlabel("Produksi (kemasan/hari)")

# Mengatur label sumbu Y, legenda, dan grid, lalu menyimpan dan menampilkan grafik
plt.ylabel("Derajat Keanggotaan"); plt.legend(); plt.grid()
plt.savefig("hasil/p3_agregasi.png", dpi=150); plt.show()

# ══════════════════════════════════════════════════════════════════════════════
# TAHAP 8: Rule Viewer — Grafik Batang Kekuatan Aktivasi Setiap Rule
# ══════════════════════════════════════════════════════════════════════════════

# Membuat grafik baru berukuran 9x4.5 inci untuk Rule Viewer
plt.figure(figsize=(9, 4.5))

# Membuat grafik batang dengan label R1–R9 pada sumbu X dan nilai alpha pada sumbu Y
plt.bar([f"R{i}" for i in range(1, 10)], alpha)

# Mengatur judul dan label sumbu untuk grafik Rule Viewer
plt.title("Rule Viewer"); plt.xlabel("Rule"); plt.ylabel("Firing Strength")

# Menampilkan grid pada sumbu Y, menyimpan gambar, dan menampilkan grafik
plt.grid(axis="y"); plt.savefig("hasil/p3_ruleviewer.png", dpi=150); plt.show()

# ══════════════════════════════════════════════════════════════════════════════
# TABEL PENGUJIAN — Menghitung produksi untuk 10 data uji sekaligus
# ══════════════════════════════════════════════════════════════════════════════

# Mendefinisikan 10 pasang data uji (permintaan, persediaan) untuk diuji secara batch
data_uji = [(1000, 100), (1500, 500), (2000, 200), (2500, 300), (3000, 350),
            (3500, 500), (4000, 600), (4500, 150), (5000, 600), (3800, 250)]

# Menampilkan header tabel hasil pengujian
print("\nNo | Permintaan | Persediaan | Produksi")

# Melakukan perulangan untuk setiap data uji, menghitung FIS, dan mencetak hasilnya
for no, (d, p) in enumerate(data_uji, 1):
    # hitung_fis(d, p)[-1] mengambil elemen terakhir (nilai hasil produksi) dari return fungsi
    print(f"{no:>2} | {d:>10} | {p:>10} | {hitung_fis(d, p)[-1]:>8.2f}")