import os
import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk, filedialog, messagebox

import numpy as np
import skfuzzy as fuzz
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

WARNA = {
    "latar": "#F1EFE8",
    "kartu": "#FFFFFF",
    "teks": "#2C2C2A",
    "teks2": "#5F5E5A",
    "garis": "#D3D1C7",
    "aksen": "#378ADD",
    "aksen_muda": "#E6F1FB",
    "aksen_teks": "#0C447C",
    "bahaya": "#E24B4A",
    "sukses_bg": "#EAF3DE",
    "sukses_teks": "#27500A",
}
WARNA_MF = ["#378ADD", "#1D9E75", "#D85A30"]

error = np.linspace(-100, 100, 201)
delta_error = np.linspace(-20, 20, 81)
pwm = np.linspace(0, 255, 256)

mf_error = {"Negatif": fuzz.trimf(error, [-100, -100, 0]),
            "Nol":     fuzz.trimf(error, [-50, 0, 50]),
            "Positif": fuzz.trimf(error, [0, 100, 100])}
mf_delta = {"Negatif": fuzz.trimf(delta_error, [-20, -20, 0]),
            "Nol":     fuzz.trimf(delta_error, [-10, 0, 10]),
            "Positif": fuzz.trimf(delta_error, [0, 20, 20])}
mf_pwm = {"Rendah": fuzz.trimf(pwm, [0, 0, 128]),
          "Sedang": fuzz.trimf(pwm, [64, 128, 192]),
          "Tinggi": fuzz.trimf(pwm, [128, 255, 255])}

RULE = [("Negatif", "Negatif", "Rendah"), ("Negatif", "Nol",     "Rendah"),
        ("Negatif", "Positif", "Sedang"), ("Nol",     "Negatif", "Rendah"),
        ("Nol",     "Nol",     "Sedang"), ("Nol",     "Positif", "Tinggi"),
        ("Positif", "Negatif", "Sedang"), ("Positif", "Nol",     "Tinggi"),
        ("Positif", "Positif", "Tinggi")]

DATA_PERCOBAAN = [
    (-80, -15),
    (-40, 0),
    (-30, 10),
    (-5, -5),
    (0, 0),
    (10, 5),
    (30, -10),
    (50, 10),
    (80, 15),
    (100, 20),
]


def hitung_fis(nilai_error, nilai_delta):
    mu_e = {k: float(fuzz.interp_membership(error, f, nilai_error)) for k, f in mf_error.items()}
    mu_d = {k: float(fuzz.interp_membership(delta_error, f, nilai_delta)) for k, f in mf_delta.items()}
    alpha = [float(np.fmin(mu_e[a], mu_d[b])) for a, b, _ in RULE]
    output_rule = [np.fmin(al, mf_pwm[c]) for al, (_, _, c) in zip(alpha, RULE)]
    aggregated = np.zeros_like(pwm, dtype=float)
    for o in output_rule:
        aggregated = np.fmax(aggregated, o)
    if aggregated.sum() > 0:
        hasil = float(fuzz.defuzz(pwm, aggregated, "centroid"))
    else:
        hasil = 0.0
    return mu_e, mu_d, alpha, output_rule, aggregated, hasil


def rapikan(ax):
    ax.set_facecolor(WARNA["kartu"])
    for sisi in ("top", "right"):
        ax.spines[sisi].set_visible(False)
    for sisi in ("left", "bottom"):
        ax.spines[sisi].set_color(WARNA["garis"])
    ax.tick_params(labelsize=7, colors=WARNA["teks2"], length=2)
    ax.grid(True, color=WARNA["garis"], alpha=0.5, lw=0.5)
    ax.set_axisbelow(True)
    ax.margins(x=0)


def plot_mf(ax, x, mf, judul, nilai, warna_garis):
    rapikan(ax)
    for (nama, f), w in zip(mf.items(), WARNA_MF):
        ax.plot(x, f, color=w, lw=1.4, label=nama)
    ax.axvline(nilai, color=warna_garis, ls="--", lw=1.2)
    ax.set_title(judul, fontsize=8.5, color=WARNA["teks"], loc="left")
    ax.set_ylim(0, 1.08)
    ax.set_yticks([0, 1])
    ax.legend(fontsize=6.5, frameon=False, ncol=3, loc="upper center",
              bbox_to_anchor=(0.5, -0.16), labelcolor=WARNA["teks2"])


def gambar(fig, nilai_error, nilai_delta, hasil_fis):
    mu_e, mu_d, alpha, output_rule, aggregated, hasil = hasil_fis
    fig.clear()
    fig.patch.set_facecolor(WARNA["kartu"])
    gs = fig.add_gridspec(5, 3, height_ratios=[1.2, 1, 1, 1, 1.5],
                          left=0.05, right=0.985, top=0.955, bottom=0.07,
                          hspace=1.05, wspace=0.28)

    plot_mf(fig.add_subplot(gs[0, 0]), error, mf_error, "Error (rpm)",
            nilai_error, WARNA["teks"])
    plot_mf(fig.add_subplot(gs[0, 1]), delta_error, mf_delta, "Delta error (rpm/siklus)",
            nilai_delta, WARNA["teks"])
    plot_mf(fig.add_subplot(gs[0, 2]), pwm, mf_pwm, "PWM motor",
            hasil, WARNA["bahaya"])

    for i, (_, _, c) in enumerate(RULE):
        ax = fig.add_subplot(gs[1 + i // 3, i % 3])
        rapikan(ax)
        ax.plot(pwm, mf_pwm[c], color=WARNA["garis"], ls="--", lw=0.9)
        ax.fill_between(pwm, output_rule[i], color=WARNA["aksen"], alpha=0.3)
        ax.plot(pwm, output_rule[i], color=WARNA["aksen"], lw=1.2)
        ax.set_title(f"R{i + 1}: {c}  (α = {alpha[i]:.2f})", fontsize=7.5,
                     color=WARNA["teks"], loc="left")
        ax.set_ylim(0, 1.08)
        ax.set_yticks([0, 1])
        ax.set_xticks([0, 128, 255])

    ax = fig.add_subplot(gs[4, :2])
    rapikan(ax)
    ax.fill_between(pwm, aggregated, color=WARNA["aksen"], alpha=0.3)
    ax.plot(pwm, aggregated, color=WARNA["aksen"], lw=1.4)
    ax.axvline(hasil, color=WARNA["bahaya"], ls="--", lw=1.4,
               label=f"Centroid = {hasil:.2f}")
    ax.set_title("Agregasi (MAX) dan defuzzifikasi centroid", fontsize=8.5,
                 color=WARNA["teks"], loc="left")
    ax.set_xlabel("PWM motor", fontsize=7.5, color=WARNA["teks2"])
    ax.set_ylim(0, 1.08)
    ax.set_yticks([0, 1])
    ax.legend(fontsize=7, frameon=False, loc="upper right", labelcolor=WARNA["teks2"])

    ax = fig.add_subplot(gs[4, 2])
    rapikan(ax)
    ax.barh(range(len(alpha)), alpha, color=WARNA["aksen"], height=0.6)
    ax.set_yticks(range(len(alpha)))
    ax.set_yticklabels([f"R{i + 1}" for i in range(len(alpha))])
    ax.invert_yaxis()
    ax.set_xlim(0, 1.2)
    ax.set_xticks([0, 0.5, 1])
    for i, a in enumerate(alpha):
        ax.text(a + 0.03, i, f"{a:.2f}", va="center", fontsize=6.5, color=WARNA["teks2"])
    ax.set_title("Rule viewer (firing strength)", fontsize=8.5,
                 color=WARNA["teks"], loc="left")


def ambil_nilai(var, batas_bawah, batas_atas):
    try:
        v = float(var.get().replace(",", "."))
    except ValueError:
        v = 0.0
    return min(batas_atas, max(batas_bawah, v))


class Aplikasi:
    def __init__(self, root):
        self.root = root
        self.tertunda = None
        self.sinkron = False
        self.keluarga = tkfont.nametofont("TkDefaultFont").actual("family")
        self.last_save_dir = os.path.abspath("hasil")
        os.makedirs("hasil", exist_ok=True)

        root.title("Pengendali Fuzzy Kecepatan Motor DC")
        root.configure(bg=WARNA["latar"])
        root.geometry("1280x800")
        root.minsize(1100, 700)

        gaya = ttk.Style()
        gaya.theme_use("clam")
        gaya.configure("Aksen.Horizontal.TProgressbar", troughcolor=WARNA["garis"],
                       background=WARNA["aksen"], bordercolor=WARNA["kartu"],
                       lightcolor=WARNA["aksen"], darkcolor=WARNA["aksen"])
        # Bentuk slider yang jelas, timbul, dan motif aksen modern
        gaya.configure("Motor.Horizontal.TScale",
                       troughcolor=WARNA["garis"],
                       background=WARNA["aksen"],
                       bordercolor="#1D6FB8",
                       lightcolor="#72B0F3",
                       darkcolor="#1D6FB8",
                       sliderlength=22,
                       sliderthickness=15)
        gaya.map("Motor.Horizontal.TScale",
                 background=[("active", "#2272BF"), ("pressed", "#14518C")])

        self.var_error = tk.StringVar(value="30")
        self.var_delta = tk.StringVar(value="5")

        self.bangun_panel_kiri()
        self.bangun_grafik()
        self.perbarui()

    def font(self, ukuran, tebal=False):
        return (self.keluarga, ukuran, "bold" if tebal else "normal")

    def kartu(self, induk):
        return tk.Frame(induk, bg=WARNA["kartu"], highlightbackground=WARNA["garis"],
                        highlightthickness=1, padx=12, pady=10)

    def bangun_panel_kiri(self):
        kiri = tk.Frame(self.root, bg=WARNA["latar"], width=330)
        kiri.pack(side="left", fill="y", padx=(14, 7), pady=14)
        kiri.pack_propagate(False)

        kepala = tk.Frame(kiri, bg=WARNA["latar"])
        kepala.pack(fill="x", pady=(0, 10))
        tk.Label(kepala, text="Pengendali fuzzy kecepatan motor DC", bg=WARNA["latar"],
                 fg=WARNA["teks"], font=self.font(12, True), anchor="w",
                 wraplength=230, justify="left").pack(side="left", anchor="n")
        tk.Label(kepala, text="Siap", bg=WARNA["sukses_bg"], fg=WARNA["sukses_teks"],
                 font=self.font(9), padx=10, pady=3).pack(side="right", anchor="n")
        tk.Label(kiri, text="Mamdani, 9 rule, defuzzifikasi centroid", bg=WARNA["latar"],
                 fg=WARNA["teks2"], font=self.font(9), anchor="w").pack(fill="x", pady=(0, 10))

        self.skala_error, self.chip_error = self.kartu_input(
            kiri, "Error (rpm)", -100, 100, self.var_error, list(mf_error))
        self.skala_delta, self.chip_delta = self.kartu_input(
            kiri, "Delta error (rpm/siklus)", -20, 20, self.var_delta, list(mf_delta))

        keluaran = self.kartu(kiri)
        keluaran.pack(fill="x", pady=(0, 10))
        tk.Label(keluaran, text="Keluaran PWM motor", bg=WARNA["kartu"], fg=WARNA["teks2"],
                 font=self.font(9), anchor="w").pack(fill="x")
        baris = tk.Frame(keluaran, bg=WARNA["kartu"])
        baris.pack(fill="x", pady=(2, 6))
        self.label_pwm = tk.Label(baris, text="0.0", bg=WARNA["kartu"], fg=WARNA["teks"],
                                  font=self.font(30, True))
        self.label_pwm.pack(side="left")
        tk.Label(baris, text=" / 255", bg=WARNA["kartu"], fg=WARNA["teks2"],
                 font=self.font(11)).pack(side="left", anchor="s", pady=6)
        self.bar_pwm = ttk.Progressbar(keluaran, maximum=255, style="Aksen.Horizontal.TProgressbar")
        self.bar_pwm.pack(fill="x")
        self.label_duty = tk.Label(keluaran, text="Duty cycle 0.0 %", bg=WARNA["kartu"],
                                   fg=WARNA["teks2"], font=self.font(9), anchor="w")
        self.label_duty.pack(fill="x", pady=(6, 0))

        baris_aksi = tk.Frame(kiri, bg=WARNA["latar"])
        baris_aksi.pack(fill="x", pady=(2, 6))
        ttk.Button(baris_aksi, text="Atur ulang", command=self.atur_ulang).pack(side="left", fill="x", expand=True, padx=(0, 4))
        ttk.Button(baris_aksi, text="💾  Simpan Gambar...", command=self.simpan_gambar).pack(side="right", fill="x", expand=True, padx=(4, 0))
        tk.Label(kiri, text="Grafik diperbarui langsung saat slider digeser atau angka diketik.",
                 bg=WARNA["latar"], fg=WARNA["teks2"], font=self.font(8),
                 wraplength=300, justify="left", anchor="w").pack(fill="x", pady=(8, 0))

    def kartu_input(self, induk, judul, batas_bawah, batas_atas, var, nama_mf):
        kartu = self.kartu(induk)
        kartu.pack(fill="x", pady=(0, 10))
        tk.Label(kartu, text=judul, bg=WARNA["kartu"], fg=WARNA["teks2"],
                 font=self.font(9), anchor="w").pack(fill="x", pady=(0, 4))

        baris = tk.Frame(kartu, bg=WARNA["kartu"])
        baris.pack(fill="x")
        skala = ttk.Scale(baris, from_=batas_bawah, to=batas_atas, orient="horizontal",
                          style="Motor.Horizontal.TScale", cursor="hand2",
                          command=lambda v: self.dari_slider(var, v))
        skala.set(float(var.get()))
        skala.pack(side="left", fill="x", expand=True)
        entri = ttk.Entry(baris, textvariable=var, width=7, justify="right")
        entri.pack(side="left", padx=(10, 0))
        entri.bind("<KeyRelease>", lambda e: self.dari_entri(var, skala, batas_bawah, batas_atas))
        entri.bind("<Return>", lambda e: self.rapikan_entri(var, skala, batas_bawah, batas_atas))
        entri.bind("<FocusOut>", lambda e: self.rapikan_entri(var, skala, batas_bawah, batas_atas))

        batas = tk.Frame(kartu, bg=WARNA["kartu"])
        batas.pack(fill="x")
        tk.Label(batas, text=str(batas_bawah), bg=WARNA["kartu"], fg=WARNA["teks2"],
                 font=self.font(8)).pack(side="left")
        tk.Label(batas, text=str(batas_atas), bg=WARNA["kartu"], fg=WARNA["teks2"],
                 font=self.font(8)).pack(side="right")

        wadah = tk.Frame(kartu, bg=WARNA["kartu"])
        wadah.pack(fill="x", pady=(8, 0))
        chip = []
        for nama in nama_mf:
            lb = tk.Label(wadah, text=nama, bg=WARNA["latar"], fg=WARNA["teks2"],
                          font=self.font(8), pady=3)
            lb.pack(side="left", fill="x", expand=True, padx=2)
            chip.append(lb)
        return skala, chip

    def bangun_grafik(self):
        kanan = tk.Frame(self.root, bg=WARNA["kartu"], highlightbackground=WARNA["garis"],
                         highlightthickness=1)
        kanan.pack(side="left", fill="both", expand=True, padx=(7, 14), pady=14)

        # Bar bawah untuk simpan grafik dan deskripsi
        bar_bawah = tk.Frame(kanan, bg=WARNA["kartu"], pady=6, padx=10)
        bar_bawah.pack(side="bottom", fill="x")
        tk.Label(bar_bawah, text="Visualisasi Lengkap FIS: MF, 9 Implikasi Aturan, Agregasi & Defuzzifikasi Centroid, Rule Viewer",
                 font=self.font(8), bg=WARNA["kartu"], fg=WARNA["teks2"]).pack(side="left")
        ttk.Button(bar_bawah, text="💾  Simpan Gambar Halaman Ini...", command=self.simpan_gambar).pack(side="right")

        self.fig = Figure(figsize=(9.5, 7.6), dpi=100)
        self.kanvas = FigureCanvasTkAgg(self.fig, master=kanan)
        self.kanvas.get_tk_widget().pack(fill="both", expand=True)

    def simpan_gambar(self):
        e = ambil_nilai(self.var_error, -100, 100)
        de = ambil_nilai(self.var_delta, -20, 20)
        default_file = f"fuzzy_motor_dc_e{int(e)}_de{int(de)}.png"
        initial_dir = self.last_save_dir if os.path.exists(self.last_save_dir) else os.path.abspath("hasil")

        fpath = filedialog.asksaveasfilename(
            parent=self.root,
            title="Simpan Gambar Grafik FIS Motor DC — Pilih Lokasi",
            initialdir=initial_dir,
            initialfile=default_file,
            defaultextension=".png",
            filetypes=[
                ("PNG Image (*.png)", "*.png"),
                ("JPEG Image (*.jpg;*.jpeg)", "*.jpg;*.jpeg"),
                ("PDF Document (*.pdf)", "*.pdf"),
                ("SVG Vector (*.svg)", "*.svg"),
                ("Semua File (*.*)", "*.*")
            ]
        )

        if not fpath:
            return

        self.last_save_dir = os.path.dirname(os.path.abspath(fpath))

        try:
            self.fig.savefig(fpath, dpi=200, bbox_inches="tight", facecolor=WARNA["kartu"])
            messagebox.showinfo(
                "Berhasil Disimpan",
                f"Gambar grafik halaman ini berhasil disimpan ke:\n\n{os.path.normpath(fpath)}"
            )
        except Exception as err:
            messagebox.showerror("Gagal Menyimpan", f"Terjadi kesalahan saat menyimpan file:\n{err}")

    def dari_slider(self, var, nilai):
        if self.sinkron:
            return
        var.set(str(int(float(nilai))))
        self.jadwalkan()

    def dari_entri(self, var, skala, batas_bawah, batas_atas):
        try:
            v = float(var.get().replace(",", "."))
        except ValueError:
            return
        self.sinkron = True
        skala.set(min(batas_atas, max(batas_bawah, v)))
        self.sinkron = False
        self.jadwalkan()

    def rapikan_entri(self, var, skala, batas_bawah, batas_atas):
        v = ambil_nilai(var, batas_bawah, batas_atas)
        var.set(f"{v:g}")
        self.sinkron = True
        skala.set(v)
        self.sinkron = False
        self.jadwalkan()

    def atur_ulang(self):
        self.var_error.set("0")
        self.var_delta.set("0")
        self.sinkron = True
        self.skala_error.set(0)
        self.skala_delta.set(0)
        self.sinkron = False
        self.perbarui()

    def jadwalkan(self):
        if self.tertunda is not None:
            self.root.after_cancel(self.tertunda)
        self.tertunda = self.root.after(30, self.perbarui)

    def perbarui_chip(self, chip, mu):
        for lb, (nama, nilai) in zip(chip, mu.items()):
            aktif = nilai > 0
            lb.configure(text=f"{nama}\n{nilai:.2f}",
                         bg=WARNA["aksen_muda"] if aktif else WARNA["latar"],
                         fg=WARNA["aksen_teks"] if aktif else WARNA["teks2"])

    def perbarui(self):
        self.tertunda = None
        nilai_error = ambil_nilai(self.var_error, -100, 100)
        nilai_delta = ambil_nilai(self.var_delta, -20, 20)
        hasil_fis = hitung_fis(nilai_error, nilai_delta)
        mu_e, mu_d, _, _, _, hasil = hasil_fis

        self.perbarui_chip(self.chip_error, mu_e)
        self.perbarui_chip(self.chip_delta, mu_d)
        self.label_pwm.configure(text=f"{hasil:.1f}")
        self.bar_pwm["value"] = hasil
        self.label_duty.configure(text=f"Duty cycle {hasil / 255 * 100:.1f} %")

        gambar(self.fig, nilai_error, nilai_delta, hasil_fis)
        self.kanvas.draw_idle()


def jalankan_pengujian_terminal():
    print("=" * 80, flush=True)
    print("   PENGUJIAN SISTEM FUZZY PENGENDALI KECEPATAN MOTOR DC (FIS MAMDANI)", flush=True)
    print("=" * 80, flush=True)
    print(f"{'No':^4} | {'Error (rpm)':^13} | {'Delta Error (rpm/s)':^21} | {'PWM (0-255)':^13} | {'Duty Cycle':^12} | {'Kategori':^10}", flush=True)
    print("-" * 80, flush=True)
    for i, (e, de) in enumerate(DATA_PERCOBAAN, 1):
        hasil_fis = hitung_fis(e, de)
        hasil_pwm = hasil_fis[-1]
        duty = (hasil_pwm / 255.0) * 100.0
        if hasil_pwm < 100:
            kat = "Rendah"
        elif hasil_pwm < 180:
            kat = "Sedang"
        else:
            kat = "Tinggi"
        print(f"{i:^4} | {e:^13} | {de:^21} | {hasil_pwm:^13.2f} | {duty:^10.2f} % | {kat:^10}", flush=True)
    print("=" * 80, flush=True)
    print("Pengujian 10 data percobaan selesai. Membuka GUI Tkinter...\n", flush=True)


def main():
    jalankan_pengujian_terminal()
    root = tk.Tk()
    Aplikasi(root)
    root.mainloop()


if __name__ == "__main__":
    main()