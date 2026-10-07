import os, sys
import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt

os.makedirs("hasil", exist_ok=True)

suhu       = np.linspace(15, 40, 251)
kelembapan = np.linspace(0, 100, 201)
durasi     = np.linspace(0, 30, 301)

mf_suhu = {"DINGIN": fuzz.trimf(suhu, [15, 15, 25]),
           "NORMAL": fuzz.trimf(suhu, [20, 27.5, 35]),
           "PANAS":  fuzz.trimf(suhu, [30, 40, 40])}
mf_kelembapan = {"KERING": fuzz.trimf(kelembapan, [0, 0, 50]),
                 "LEMBAP": fuzz.trimf(kelembapan, [25, 50, 75]),
                 "BASAH":  fuzz.trimf(kelembapan, [50, 100, 100])}
mf_durasi = {"SINGKAT": fuzz.trimf(durasi, [0, 0, 12]),
             "SEDANG":  fuzz.trimf(durasi, [8, 15, 22]),
             "LAMA":    fuzz.trimf(durasi, [18, 30, 30])}

RULE = [("DINGIN", "KERING", "SEDANG"), ("DINGIN", "LEMBAP", "SINGKAT"),
        ("DINGIN", "BASAH",  "SINGKAT"), ("NORMAL", "KERING", "LAMA"),
        ("NORMAL", "LEMBAP", "SEDANG"),  ("NORMAL", "BASAH",  "SINGKAT"),
        ("PANAS",  "KERING", "LAMA"),    ("PANAS",  "LEMBAP", "LAMA"),
        ("PANAS",  "BASAH",  "SEDANG")]

def hitung_fis(nilai_suhu, nilai_kelembapan):
    mu_s = {k: fuzz.interp_membership(suhu, f, nilai_suhu) for k, f in mf_suhu.items()}
    mu_k = {k: fuzz.interp_membership(kelembapan, f, nilai_kelembapan) for k, f in mf_kelembapan.items()}
    alpha = [np.fmin(mu_s[a], mu_k[b]) for a, b, _ in RULE]
    output_rule = [np.fmin(al, mf_durasi[c]) for al, (_, _, c) in zip(alpha, RULE)]
    aggregated = np.zeros_like(durasi, dtype=float)
    for o in output_rule:
        aggregated = np.fmax(aggregated, o)
    if aggregated.sum() == 0:
        sys.exit("Agregasi kosong, input di luar semesta.")
    hasil = fuzz.defuzz(durasi, aggregated, "centroid")
    return mu_s, mu_k, alpha, output_rule, aggregated, hasil

nilai_suhu       = float(input("Suhu (15-40 C)         : "))
nilai_kelembapan = float(input("Kelembapan tanah (0-100): "))
if not (15 <= nilai_suhu <= 40 and 0 <= nilai_kelembapan <= 100):
    sys.exit("Input di luar semesta pembicaraan.")
mu_s, mu_k, alpha, output_rule, aggregated, hasil = hitung_fis(nilai_suhu, nilai_kelembapan)

print("\n== FUZZIFIKASI SUHU ==")
for k, v in mu_s.items(): print(f"{k:<8} = {v:.4f}")
print("\n== FUZZIFIKASI KELEMBAPAN ==")
for k, v in mu_k.items(): print(f"{k:<8} = {v:.4f}")
print("\n== FIRING STRENGTH ==")
for i, (a, b, c) in enumerate(RULE, 1):
    print(f"R{i}: IF {a} AND {b} THEN {c:<7} -> alpha = {alpha[i-1]:.4f}")
print(f"\nHASIL DURASI = {hasil:.2f} menit")

fig, axs = plt.subplots(1, 3, figsize=(16, 4.5))
for ax, (x, mf, judul, nilai) in zip(axs, [
        (suhu,       mf_suhu,       "Suhu (°C)",             nilai_suhu),
        (kelembapan, mf_kelembapan, "Kelembapan Tanah (%)",  nilai_kelembapan),
        (durasi,     mf_durasi,     "Durasi (menit)",        None)]):
    for nama, f in mf.items():
        ax.plot(x, f, label=nama)
    if nilai is not None:
        ax.axvline(nilai, color="k", linestyle="--", label=f"Input = {nilai:g}")
    ax.set_title(f"Membership Function {judul}")
    ax.set_xlabel(judul); ax.set_ylabel("Derajat Keanggotaan"); ax.grid(); ax.legend()
plt.tight_layout(); plt.savefig("hasil/p4_membership.png", dpi=150); plt.show()

fig, axs = plt.subplots(3, 3, figsize=(14, 9), sharex=True, sharey=True)
for i, ax in enumerate(axs.ravel()):
    ax.fill_between(durasi, output_rule[i], alpha=0.4)
    ax.set_title(f"R{i+1} (alpha = {alpha[i]:.2f})"); ax.grid()
fig.suptitle("Implikasi (MIN) setiap rule")
plt.tight_layout(); plt.savefig("hasil/p4_implikasi.png", dpi=150); plt.show()

plt.figure(figsize=(9, 4.5))
plt.fill_between(durasi, aggregated, alpha=0.4, label="Agregasi (MAX)")
plt.axvline(hasil, color="r", linestyle="--", label=f"Centroid = {hasil:.2f}")
plt.title("Agregasi dan Defuzzifikasi"); plt.xlabel("Durasi Penyiraman (menit)")
plt.ylabel("Derajat Keanggotaan"); plt.legend(); plt.grid()
plt.savefig("hasil/p4_agregasi.png", dpi=150); plt.show()

plt.figure(figsize=(9, 4.5))
plt.bar([f"R{i}" for i in range(1, 10)], alpha)
plt.title("Rule Viewer"); plt.xlabel("Rule"); plt.ylabel("Firing Strength")
plt.grid(axis="y"); plt.savefig("hasil/p4_ruleviewer.png", dpi=150); plt.show()

data_uji = [(16, 10), (18, 45), (22, 80), (27, 20), (28, 50),
            (30, 90), (35, 15), (36, 55), (39, 70), (32, 40)]
print("\nNo | Suhu (C) | Kelembapan (%) | Durasi (menit)")
for no, (s, k) in enumerate(data_uji, 1):
    print(f"{no:>2} | {s:>8} | {k:>14} | {hitung_fis(s, k)[-1]:>14.2f}")