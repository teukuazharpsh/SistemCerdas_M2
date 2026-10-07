# Mengimpor modul os untuk operasi sistem file (seperti pembuatan folder)
import os

# Mengimpor modul numpy untuk membuat array numerik dan operasi matematika
import numpy as np

# Mengimpor modul scikit-fuzzy untuk perhitungan logika fuzzy dan fungsi keanggotaan
import skfuzzy as fuzz

# Mengimpor matplotlib.pyplot untuk visualisasi data dalam bentuk grafik
import matplotlib.pyplot as plt

# Membuat folder 'hasil' jika belum tersedia untuk menyimpan file output grafik
os.makedirs("hasil", exist_ok=True)

# Mendefinisikan semesta pembicaraan (universe of discourse) nilai pelayanan dari 0 hingga 10 dengan interval 0.1
pelayanan = np.arange(0, 10.1, 0.1)

# Membuat fungsi keanggotaan segitiga (triangular) untuk kategori "MENGECEWAKAN" dengan parameter [a=0, b=0, c=5]
pelayanan_mengecewakan = fuzz.trimf(pelayanan, [0, 0, 5])

# Membuat fungsi keanggotaan segitiga untuk kategori "MEMUASKAN" dengan parameter [a=5, b=10, c=10]
pelayanan_memuaskan    = fuzz.trimf(pelayanan, [5, 10, 10])

# Mendefinisikan dictionary untuk membandingkan dua variasi kurva fungsi keanggotaan "BAGUS"
variasi = {
    # Variasi 1: Bentuk kurva segitiga awal simetris dengan titik sudut [2.5, 5, 7.5]
    "Awal: BAGUS [2.5, 5, 7.5]":   fuzz.trimf(pelayanan, [2.5, 5, 7.5]),
    # Variasi 2: Bentuk kurva segitiga hasil modifikasi dengan titik sudut [3, 5, 8]
    "Modifikasi: BAGUS [3, 5, 8]": fuzz.trimf(pelayanan, [3, 5, 8]),
}

# Membuat kanvas grafik berukuran 14x5 inci dengan 1 baris dan 2 kolom serta berbagi skala sumbu Y yang sama
fig, axs = plt.subplots(1, 2, figsize=(14, 5), sharey=True)

# Melakukan perulangan untuk menampilkan visualisasi grafik pada masing-masing subplot
for ax, (judul, bagus) in zip(axs, variasi.items()):
    # Menggambar kurva fungsi keanggotaan kategori MENGECEWAKAN
    ax.plot(pelayanan, pelayanan_mengecewakan, label="MENGECEWAKAN")
    # Menggambar kurva fungsi keanggotaan kategori BAGUS sesuai variasi
    ax.plot(pelayanan, bagus, label="BAGUS")
    # Menggambar kurva fungsi keanggotaan kategori MEMUASKAN
    ax.plot(pelayanan, pelayanan_memuaskan, label="MEMUASKAN")
    # Mengatur judul subplot
    ax.set_title(judul)
    # Mengatur label pada sumbu X
    ax.set_xlabel("Nilai Pelayanan")
    # Menampilkan garis kisi (grid) pada grafik
    ax.grid()
    # Menampilkan legenda (keterangan label kurva)
    ax.legend()

# Menambahkan label pada sumbu Y untuk subplot pertama (Derajat Keanggotaan / μ)
axs[0].set_ylabel("Derajat Keanggotaan")

# Mengatur tata letak agar elemen grafik rapi dan tidak bertumpukan
plt.tight_layout()

# Menyimpan gambar grafik yang telah dibuat ke dalam folder hasil dengan resolusi 150 DPI
plt.savefig("hasil/p1_membership.png", dpi=150)

# Menampilkan jendela grafik visualisasi
plt.show()

# Melakukan perulangan untuk melakukan fuzzifikasi (evaluasi nilai keanggotaan) pada setiap variasi
for judul, bagus in variasi.items():
    # Menampilkan judul variasi yang sedang dihitung
    print(judul)
    # Melakukan perulangan untuk setiap nilai input uji (crisp input)
    for nilai in [3, 4, 6, 7]:
        # Menghitung derajat keanggotaan untuk kategori MENGECEWAKAN pada nilai uji menggunakan interpolasi
        m = fuzz.interp_membership(pelayanan, pelayanan_mengecewakan, nilai)
        # Menghitung derajat keanggotaan untuk kategori BAGUS pada nilai uji menggunakan interpolasi
        b = fuzz.interp_membership(pelayanan, bagus, nilai)
        # Menghitung derajat keanggotaan untuk kategori MEMUASKAN pada nilai uji menggunakan interpolasi
        u = fuzz.interp_membership(pelayanan, pelayanan_memuaskan, nilai)
        # Mencetak hasil derajat keanggotaan untuk masing-masing kategori dengan format 3 angka desimal
        print(f"  x={nilai}: MENGECEWAKAN={m:.3f} BAGUS={b:.3f} MEMUASKAN={u:.3f}")