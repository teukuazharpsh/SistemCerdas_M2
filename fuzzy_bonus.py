# Mengimpor modul os untuk operasi sistem file (membuat folder) dan sys untuk menghentikan program
import os, sys

# Mengimpor numpy untuk perhitungan array numerik dan operasi matematika vektor
import numpy as np

# Mengimpor scikit-fuzzy untuk fungsi keanggotaan fuzzy dan operasi logika fuzzy
import skfuzzy as fuzz

# Mengimpor matplotlib untuk membuat grafik visualisasi
import matplotlib.pyplot as plt

# Membuat folder 'hasil' jika belum ada, tempat menyimpan gambar output grafik
os.makedirs("hasil", exist_ok=True)

# Mendefinisikan semesta pembicaraan (universe) untuk variabel PELAYANAN: rentang 0–10, langkah 0.1
pelayanan = np.arange(0, 10.1, 0.1)

# Mendefinisikan semesta pembicaraan untuk variabel MAKANAN: rentang 0–10, langkah 0.1
makanan   = np.arange(0, 10.1, 0.1)

# Mendefinisikan semesta pembicaraan untuk variabel output BONUS: rentang 0–30, langkah 0.1
bonus     = np.arange(0, 30.1, 0.1)

# ──────────────────────────────────────────────────────────────────────────────
# DEFINISI FUNGSI KEANGGOTAAN (Membership Functions) menggunakan kurva SEGITIGA
# ──────────────────────────────────────────────────────────────────────────────

# Fungsi keanggotaan MENGECEWAKAN: segitiga dengan titik [a=0, b=0, c=5]
# → bernilai 1 di x=0, turun ke 0 di x=5
pelayanan_mengecewakan = fuzz.trimf(pelayanan, [0, 0, 5])

# Fungsi keanggotaan BAGUS: segitiga simetris dengan titik [a=2.5, b=5, c=7.5]
# → puncak (nilai 1) berada di x=5
pelayanan_bagus        = fuzz.trimf(pelayanan, [2.5, 5, 7.5])

# Fungsi keanggotaan MEMUASKAN: segitiga dengan titik [a=5, b=10, c=10]
# → naik dari 0 di x=5, mencapai 1 di x=10
pelayanan_memuaskan    = fuzz.trimf(pelayanan, [5, 10, 10])

# Fungsi keanggotaan HAMBAR: segitiga dengan titik [-4, 0, 7]
# → puncak di x=0, melebar ke kanan hingga x=7
makanan_hambar = fuzz.trimf(makanan, [-4, 0, 7])

# Fungsi keanggotaan ENAK: segitiga dengan titik [3, 10, 14]
# → naik dari x=3, puncak di x=10, turun hingga x=14
makanan_enak   = fuzz.trimf(makanan, [3, 10, 14])

# Fungsi keanggotaan bonus SEDIKIT: segitiga [0, 5, 10] → bonus kecil
bonus_sedikit = fuzz.trimf(bonus, [0, 5, 10])

# Fungsi keanggotaan bonus SEDANG: segitiga [10, 15, 20] → bonus menengah
bonus_sedang  = fuzz.trimf(bonus, [10, 15, 20])

# Fungsi keanggotaan bonus BANYAK: segitiga [20, 25, 30] → bonus besar
bonus_banyak  = fuzz.trimf(bonus, [20, 25, 30])

# ──────────────────────────────────────────────────────────────────────────────
# INPUT NILAI CRISP dari pengguna (nilai nyata sebelum difuzzifikasi)
# ──────────────────────────────────────────────────────────────────────────────

# Menerima input nilai pelayanan dari pengguna (0–10) dan mengubahnya ke float
nilai_pelayanan = float(input("Nilai pelayanan (0-10): "))

# Menerima input nilai makanan dari pengguna (0–10) dan mengubahnya ke float
nilai_makanan   = float(input("Nilai makanan   (0-10): "))

# ══════════════════════════════════════════════════════════════════════════════
# TAHAP 1: Visualisasi grafik fungsi keanggotaan + garis input (crisp input)
# ══════════════════════════════════════════════════════════════════════════════

# Membuat kanvas dengan 3 subplot berdampingan berukuran 16x4.5 inci
fig, axs = plt.subplots(1, 3, figsize=(16, 4.5))

# Melakukan perulangan untuk menggambar masing-masing grafik (Pelayanan, Makanan, Bonus)
for ax, (x, mfs, judul, nilai) in zip(axs, [
    # Subplot 1: fungsi keanggotaan Pelayanan dengan garis input
    (pelayanan, {"MENGECEWAKAN": pelayanan_mengecewakan, "BAGUS": pelayanan_bagus,
                 "MEMUASKAN": pelayanan_memuaskan}, "Pelayanan", nilai_pelayanan),
    # Subplot 2: fungsi keanggotaan Makanan dengan garis input
    (makanan, {"HAMBAR": makanan_hambar, "ENAK": makanan_enak}, "Makanan", nilai_makanan),
    # Subplot 3: fungsi keanggotaan Bonus (tanpa garis input karena ini output)
    (bonus, {"SEDIKIT": bonus_sedikit, "SEDANG": bonus_sedang,
             "BANYAK": bonus_banyak}, "Bonus", None)]):

    # Menggambar setiap kurva fungsi keanggotaan pada subplot
    for nama, f in mfs.items():
        ax.plot(x, f, label=nama)

    # Jika ada nilai input (bukan None), gambar garis vertikal penanda posisi input
    if nilai is not None:
        ax.axvline(nilai, color="k", linestyle="--", label=f"Input = {nilai:g}")

    # Mengatur judul, grid, dan legenda untuk setiap subplot
    ax.set_title(f"MF {judul}"); ax.grid(); ax.legend()

# Mengatur tata letak rapi, menyimpan gambar, lalu menampilkannya
plt.tight_layout(); plt.savefig("hasil/p2_membership.png", dpi=150); plt.show()

# ══════════════════════════════════════════════════════════════════════════════
# TAHAP 2–3: Fuzzifikasi — mengubah nilai crisp menjadi derajat keanggotaan (μ)
# ══════════════════════════════════════════════════════════════════════════════

# Menghitung μ (derajat keanggotaan) nilai pelayanan untuk kategori MENGECEWAKAN
mu_mengecewakan = fuzz.interp_membership(pelayanan, pelayanan_mengecewakan, nilai_pelayanan)

# Menghitung μ nilai pelayanan untuk kategori BAGUS
mu_bagus        = fuzz.interp_membership(pelayanan, pelayanan_bagus, nilai_pelayanan)

# Menghitung μ nilai pelayanan untuk kategori MEMUASKAN
mu_memuaskan    = fuzz.interp_membership(pelayanan, pelayanan_memuaskan, nilai_pelayanan)

# Menghitung μ nilai makanan untuk kategori HAMBAR
mu_hambar = fuzz.interp_membership(makanan, makanan_hambar, nilai_makanan)

# Menghitung μ nilai makanan untuk kategori ENAK
mu_enak   = fuzz.interp_membership(makanan, makanan_enak, nilai_makanan)

# Menampilkan seluruh hasil fuzzifikasi ke layar dengan format 4 angka desimal
print(f"MENGECEWAKAN = {mu_mengecewakan:.4f}\nBAGUS        = {mu_bagus:.4f}\n"
      f"MEMUASKAN    = {mu_memuaskan:.4f}\nHAMBAR       = {mu_hambar:.4f}\n"
      f"ENAK         = {mu_enak:.4f}")

# ══════════════════════════════════════════════════════════════════════════════
# TAHAP 4: Evaluasi Rule (Aturan IF-THEN) menggunakan operator AND = MIN
# Setiap alpha (α) adalah "firing strength" atau kekuatan aktifasi aturan
# ══════════════════════════════════════════════════════════════════════════════

# R1: IF pelayanan MENGECEWAKAN AND makanan HAMBAR → THEN bonus SEDIKIT
alpha1 = np.fmin(mu_mengecewakan, mu_hambar)   # R1 -> SEDIKIT

# R2: IF pelayanan MENGECEWAKAN AND makanan ENAK → THEN bonus SEDIKIT
alpha2 = np.fmin(mu_mengecewakan, mu_enak)     # R2 -> SEDIKIT

# R3: IF pelayanan BAGUS AND makanan HAMBAR → THEN bonus SEDIKIT
alpha3 = np.fmin(mu_bagus, mu_hambar)          # R3 -> SEDIKIT

# R4: IF pelayanan BAGUS AND makanan ENAK → THEN bonus SEDANG
alpha4 = np.fmin(mu_bagus, mu_enak)            # R4 -> SEDANG

# R5: IF pelayanan MEMUASKAN AND makanan HAMBAR → THEN bonus SEDANG
alpha5 = np.fmin(mu_memuaskan, mu_hambar)      # R5 -> SEDANG

# R6: IF pelayanan MEMUASKAN AND makanan ENAK → THEN bonus BANYAK
alpha6 = np.fmin(mu_memuaskan, mu_enak)        # R6 -> BANYAK

# ══════════════════════════════════════════════════════════════════════════════
# TAHAP 5: Implikasi — memotong kurva output sesuai nilai alpha (metode MIN)
# Hasilnya adalah kurva output yang "dipangkas" pada ketinggian alpha
# ══════════════════════════════════════════════════════════════════════════════

# Implikasi R1: memotong kurva bonus SEDIKIT di ketinggian alpha1
output_r1 = np.fmin(alpha1, bonus_sedikit)

# Implikasi R2: memotong kurva bonus SEDIKIT di ketinggian alpha2
output_r2 = np.fmin(alpha2, bonus_sedikit)

# Implikasi R3: memotong kurva bonus SEDIKIT di ketinggian alpha3
output_r3 = np.fmin(alpha3, bonus_sedikit)

# Implikasi R4: memotong kurva bonus SEDANG di ketinggian alpha4
output_r4 = np.fmin(alpha4, bonus_sedang)

# Implikasi R5: memotong kurva bonus SEDANG di ketinggian alpha5
output_r5 = np.fmin(alpha5, bonus_sedang)

# Implikasi R6: memotong kurva bonus BANYAK di ketinggian alpha6
output_r6 = np.fmin(alpha6, bonus_banyak)

# ══════════════════════════════════════════════════════════════════════════════
# TAHAP 6: Agregasi — menggabungkan semua output rule menggunakan operasi MAX
# Mengambil nilai tertinggi dari semua kurva implikasi di setiap titik
# ══════════════════════════════════════════════════════════════════════════════

# Mulai agregasi dari output rule pertama
aggregated = output_r1

# Gabungkan output rule berikutnya satu per satu menggunakan MAX (fmax)
for o in (output_r2, output_r3, output_r4, output_r5, output_r6):
    aggregated = np.fmax(aggregated, o)

# ══════════════════════════════════════════════════════════════════════════════
# TAHAP 7: Defuzzifikasi — mengubah kurva agregasi menjadi nilai crisp (angka)
# Menggunakan metode CENTROID (pusat massa / center of gravity)
# ══════════════════════════════════════════════════════════════════════════════

# Jika hasil agregasi seluruhnya 0 (tidak ada rule yang aktif), hentikan program
if aggregated.sum() == 0:
    sys.exit("Agregasi kosong, input di luar semesta.")

# Menghitung nilai crisp bonus menggunakan metode centroid dari kurva agregasi
hasil_bonus = fuzz.defuzz(bonus, aggregated, "centroid")

# Menampilkan nilai bonus akhir ke layar dengan format 2 angka desimal
print(f"HASIL BONUS = {hasil_bonus:.2f}")

# Membuat grafik baru berukuran 9x4.5 inci untuk visualisasi implikasi dan agregasi
plt.figure(figsize=(9, 4.5))

# Menggambar kurva implikasi setiap rule dengan garis titik-titik (dotted)
for i, o in enumerate((output_r1, output_r2, output_r3, output_r4, output_r5, output_r6), 1):
    plt.plot(bonus, o, linestyle=":", label=f"R{i}")

# Menggambar area agregasi (union semua kurva implikasi) dengan transparansi (alpha=0.3)
plt.fill_between(bonus, aggregated, alpha=0.3, label="Agregasi")

# Menggambar garis vertikal merah penanda nilai centroid (hasil defuzzifikasi)
plt.axvline(hasil_bonus, color="r", linestyle="--", label=f"Centroid = {hasil_bonus:.2f}")

# Mengatur judul, label sumbu, grid, dan legenda grafik agregasi
plt.title("Implikasi, Agregasi, dan Defuzzifikasi"); plt.xlabel("Bonus")

# Menampilkan grid, legenda, menyimpan grafik, lalu menampilkannya
plt.grid(); plt.legend(); plt.savefig("hasil/p2_agregasi.png", dpi=150); plt.show()

# ══════════════════════════════════════════════════════════════════════════════
# TAHAP 8: Rule Viewer — menampilkan kekuatan aktivasi (firing strength) tiap rule
# ══════════════════════════════════════════════════════════════════════════════

# Mendefinisikan label nama setiap rule untuk sumbu X grafik batang
nama_rule  = ["R1", "R2", "R3", "R4", "R5", "R6"]

# Mendefinisikan nilai alpha (firing strength) masing-masing rule
nilai_alpha = [alpha1, alpha2, alpha3, alpha4, alpha5, alpha6]

# Membuat grafik batang (bar chart) untuk memvisualisasikan kekuatan setiap rule
plt.bar(nama_rule, nilai_alpha)

# Mengatur judul dan label sumbu untuk grafik Rule Viewer
plt.title("Rule Viewer"); plt.xlabel("Rule"); plt.ylabel("Firing Strength")

# Menampilkan grid hanya pada sumbu Y, menyimpan gambar, lalu menampilkan grafik
plt.grid(axis="y"); plt.savefig("hasil/p2_ruleviewer.png", dpi=150); plt.show()