"""
fuzzy_penyiraman_gui.py  —  v3
GUI Sistem Fuzzy Penyiraman Tanaman (FIS Mamdani)
Fitur:
- Dua cara input: Slider interaktif & Input Manual (Entry keyboard) tersinkronisasi
- Simpan gambar grafik dengan File Explorer kustom (pilih folder & nama file bebas)
- Visualisasi lengkap: MF, Implikasi, Agregasi & Defuzzifikasi, Rule Viewer
- Tabel 10 data uji otomatis

MKPT 501 — Sistem Cerdas | Modul 2
"""

import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import numpy as np
import skfuzzy as fuzz
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.gridspec as gridspec

# Buat folder default untuk penyimpanan jika belum ada
os.makedirs("hasil", exist_ok=True)

# ───────────────────────────────────────────────────
# FUZZY: semesta, MF, rule
# ───────────────────────────────────────────────────
suhu       = np.linspace(15, 40, 251)
kelembapan = np.linspace(0,  100, 201)
durasi     = np.linspace(0,  30,  301)

mf_suhu = {
    "DINGIN": fuzz.trimf(suhu, [15, 15, 25]),
    "NORMAL": fuzz.trimf(suhu, [20, 27.5, 35]),
    "PANAS":  fuzz.trimf(suhu, [30, 40, 40]),
}
mf_kelembapan = {
    "KERING": fuzz.trimf(kelembapan, [0,   0,  50]),
    "LEMBAP": fuzz.trimf(kelembapan, [25, 50,  75]),
    "BASAH":  fuzz.trimf(kelembapan, [50, 100, 100]),
}
mf_durasi = {
    "SINGKAT": fuzz.trimf(durasi, [0,  0,  12]),
    "SEDANG":  fuzz.trimf(durasi, [8,  15, 22]),
    "LAMA":    fuzz.trimf(durasi, [18, 30, 30]),
}
RULE = [
    ("DINGIN", "KERING", "SEDANG"),  ("DINGIN", "LEMBAP", "SINGKAT"),
    ("DINGIN", "BASAH",  "SINGKAT"), ("NORMAL", "KERING", "LAMA"),
    ("NORMAL", "LEMBAP", "SEDANG"),  ("NORMAL", "BASAH",  "SINGKAT"),
    ("PANAS",  "KERING", "LAMA"),    ("PANAS",  "LEMBAP", "LAMA"),
    ("PANAS",  "BASAH",  "SEDANG"),
]
DATA_UJI = [(16,10),(18,45),(22,80),(27,20),(28,50),
            (30,90),(35,15),(36,55),(39,70),(32,40)]

def hitung_fis(ns, nk):
    mu_s = {k: fuzz.interp_membership(suhu, f, ns)       for k, f in mf_suhu.items()}
    mu_k = {k: fuzz.interp_membership(kelembapan, f, nk) for k, f in mf_kelembapan.items()}
    alpha_l  = [np.fmin(mu_s[a], mu_k[b]) for a, b, _ in RULE]
    out_rule = [np.fmin(al, mf_durasi[c]) for al, (_, _, c) in zip(alpha_l, RULE)]
    agg = np.zeros_like(durasi, dtype=float)
    for o in out_rule:
        agg = np.fmax(agg, o)
    hasil = fuzz.defuzz(durasi, agg, "centroid") if agg.sum() > 0 else 0.0
    return mu_s, mu_k, alpha_l, out_rule, agg, hasil


# ───────────────────────────────────────────────────
# APLIKASI GUI
# ───────────────────────────────────────────────────
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistem Fuzzy Penyiraman Tanaman — FIS Mamdani")
        self.geometry("1180x740")
        self.minsize(1000, 650)
        self.resizable(True, True)
        self.configure(bg="#f4f4f6")

        self.result = None          # simpan hasil perhitungan terakhir
        self.last_save_dir = os.path.abspath("hasil")  # ingat folder simpan terakhir
        self._sync_lock = True      # kunci selama pembuatan widget agar callback slider tidak error
        self._build()
        self._sync_lock = False

        # Aktifkan scroll roda mouse di panel kiri
        self.bind_all("<MouseWheel>", self._on_mousewheel)

        # Jalankan perhitungan awal dengan nilai default
        self._hitung(from_entry=True)

    # ── Scroll roda mouse untuk panel kiri ─────────
    def _on_mousewheel(self, event):
        if hasattr(self, 'left_container') and hasattr(self, 'canvas_left'):
            try:
                x, y = self.winfo_pointerxy()
                w = self.winfo_containing(x, y)
                cur = w
                while cur is not None:
                    if cur == self.left_container:
                        self.canvas_left.yview_scroll(int(-1 * (event.delta / 120)), "units")
                        return
                    cur = getattr(cur, "master", None)
            except Exception:
                pass

    # ── bangun UI ──────────────────────────────────
    def _build(self):
        # ── Header ────────────────────────────────
        hdr = tk.Frame(self, bg="#f4f4f6")
        hdr.pack(fill="x", padx=18, pady=(10, 4))

        hdr_info = tk.Frame(hdr, bg="#f4f4f6")
        hdr_info.pack(side="left")

        tk.Label(hdr_info, text="Sistem Fuzzy Penyiraman Tanaman",
                 font=("Segoe UI", 15, "bold"), bg="#f4f4f6", fg="#1e293b"
                 ).pack(anchor="w")
        tk.Label(hdr_info, text="FIS Mamdani  ·  MKPT 501 Sistem Cerdas  ·  Dua Metode Input & Export Gambar Bebas",
                 font=("Segoe UI", 9), bg="#f4f4f6", fg="#64748b"
                 ).pack(anchor="w")

        # Tombol Simpan Semua Bagian Terpisah (.PNG)
        btn_save_all = ttk.Button(
            hdr,
            text="📁  Simpan Semua Bagian (Pisah Tiap File .PNG)...",
            command=self._simpan_semua_bagian_terpisah
        )
        btn_save_all.pack(side="right", pady=4)

        ttk.Separator(self).pack(fill="x", padx=16, pady=(4, 6))

        # ── Badan Utama ───────────────────────────
        body = tk.Frame(self, bg="#f4f4f6")
        body.pack(fill="both", expand=True, padx=14, pady=(0, 8))

        self._build_left(body)
        self._build_right(body)

    # ── Panel Kiri: Kontrol & Hasil ───────────────
    def _build_left(self, parent):
        # Container dengan scrollbar vertikal agar pas di semua resolusi layar
        self.left_container = tk.Frame(parent, bg="#f4f4f6", width=360)
        self.left_container.pack(side="left", fill="y", padx=(0, 10))
        self.left_container.pack_propagate(False)

        # Scrollbar vertikal: di-pack lebih dulu ke kanan agar selalu muncul
        self.sb_left = ttk.Scrollbar(self.left_container, orient="vertical")
        self.sb_left.pack(side="right", fill="y")

        self.canvas_left = tk.Canvas(self.left_container, bg="#f4f4f6", highlightthickness=0,
                                     yscrollcommand=self.sb_left.set)
        self.canvas_left.pack(side="left", fill="both", expand=True)
        self.sb_left.configure(command=self.canvas_left.yview)

        self.scrollable_frame = tk.Frame(self.canvas_left, bg="#f4f4f6")
        self.canvas_window = self.canvas_left.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        def _on_frame_configure(event=None):
            self.canvas_left.configure(scrollregion=self.canvas_left.bbox("all"))

        def _on_canvas_configure(event):
            self.canvas_left.itemconfig(self.canvas_window, width=event.width)

        self.scrollable_frame.bind("<Configure>", _on_frame_configure)
        self.canvas_left.bind("<Configure>", _on_canvas_configure)

        lf = tk.LabelFrame(self.scrollable_frame, text=" Kontrol Input & Hasil ",
                           font=("Segoe UI", 9, "bold"),
                           bg="#ffffff", fg="#1e293b", padx=10, pady=8,
                           relief="groove", bd=1)
        lf.pack(fill="x", padx=2, pady=2)

        # ── INPUT 1: SUHU (Slider + Entry) ────────
        box_suhu = tk.LabelFrame(lf, text=" 🌡️ Suhu Udara (15 – 40 °C) ",
                                 font=("Segoe UI", 9, "bold"),
                                 bg="#ffffff", fg="#0284c7", padx=8, pady=6)
        box_suhu.pack(fill="x", pady=(2, 8))

        f_ent_s = tk.Frame(box_suhu, bg="#ffffff")
        f_ent_s.pack(fill="x", pady=(0, 4))
        tk.Label(f_ent_s, text="Ketik Manual:", font=("Segoe UI", 8),
                 bg="#ffffff", fg="#475569").pack(side="left")
        self.ent_suhu = ttk.Entry(f_ent_s, width=8, font=("Segoe UI", 9))
        self.ent_suhu.insert(0, "27.0")
        self.ent_suhu.pack(side="left", padx=(6, 4))
        tk.Label(f_ent_s, text="°C", font=("Segoe UI", 8, "bold"),
                 bg="#ffffff", fg="#475569").pack(side="left")

        # Tombol setel dari teks jika diketik
        ttk.Button(f_ent_s, text="Terapkan", width=8,
                   command=lambda: self._on_entry_changed("suhu")
                   ).pack(side="right")
        self.ent_suhu.bind("<Return>", lambda e: self._on_entry_changed("suhu"))

        # Slider Suhu
        f_sl_s = tk.Frame(box_suhu, bg="#ffffff")
        f_sl_s.pack(fill="x")
        self.slider_suhu = ttk.Scale(f_sl_s, from_=15.0, to=40.0,
                                     orient="horizontal",
                                     command=self._on_slider_suhu)
        self.slider_suhu.set(27.0)
        self.slider_suhu.pack(side="left", fill="x", expand=True, padx=(0, 6))

        # ── INPUT 2: KELEMBAPAN (Slider + Entry) ──
        box_kel = tk.LabelFrame(lf, text=" 💧 Kelembapan Tanah (0 – 100 %) ",
                                font=("Segoe UI", 9, "bold"),
                                bg="#ffffff", fg="#0284c7", padx=8, pady=6)
        box_kel.pack(fill="x", pady=(0, 8))

        f_ent_k = tk.Frame(box_kel, bg="#ffffff")
        f_ent_k.pack(fill="x", pady=(0, 4))
        tk.Label(f_ent_k, text="Ketik Manual:", font=("Segoe UI", 8),
                 bg="#ffffff", fg="#475569").pack(side="left")
        self.ent_kel = ttk.Entry(f_ent_k, width=8, font=("Segoe UI", 9))
        self.ent_kel.insert(0, "50.0")
        self.ent_kel.pack(side="left", padx=(6, 4))
        tk.Label(f_ent_k, text="%", font=("Segoe UI", 8, "bold"),
                 bg="#ffffff", fg="#475569").pack(side="left")

        # Tombol setel dari teks jika diketik
        ttk.Button(f_ent_k, text="Terapkan", width=8,
                   command=lambda: self._on_entry_changed("kel")
                   ).pack(side="right")
        self.ent_kel.bind("<Return>", lambda e: self._on_entry_changed("kel"))

        # Slider Kelembapan
        f_sl_k = tk.Frame(box_kel, bg="#ffffff")
        f_sl_k.pack(fill="x")
        self.slider_kel = ttk.Scale(f_sl_k, from_=0.0, to=100.0,
                                    orient="horizontal",
                                    command=self._on_slider_kel)
        self.slider_kel.set(50.0)
        self.slider_kel.pack(side="left", fill="x", expand=True, padx=(0, 6))

        # ── Tombol Hitung Ulang ────────────────────
        ttk.Button(lf, text="⚡  Hitung FIS Ulang  ⚡",
                   command=lambda: self._hitung(from_entry=True)
                   ).pack(fill="x", pady=(2, 8))
        ttk.Separator(lf).pack(fill="x", pady=4)

        # ── HASIL DURASI ──────────────────────────
        res_frame = tk.Frame(lf, bg="#f8fafc", relief="solid", bd=1, padx=6, pady=6)
        res_frame.pack(fill="x", pady=4)

        tk.Label(res_frame, text="Hasil Durasi Penyiraman:",
                 font=("Segoe UI", 8, "bold"), bg="#f8fafc", fg="#475569"
                 ).pack(anchor="w")
        self.lbl_hasil = tk.Label(res_frame, text="—",
                                   font=("Segoe UI", 20, "bold"),
                                   bg="#f8fafc", fg="#15803d")
        self.lbl_hasil.pack(pady=2)
        self.lbl_kat = tk.Label(res_frame, text="", font=("Segoe UI", 9, "italic"),
                                 bg="#f8fafc", fg="#64748b")
        self.lbl_kat.pack()

        ttk.Separator(lf).pack(fill="x", pady=6)

        # ── FUZZIFIKASI ───────────────────────────
        tk.Label(lf, text="Derajat Keanggotaan (μ)",
                 font=("Segoe UI", 9, "bold"), bg="#ffffff", fg="#1e293b"
                 ).pack(anchor="w")
        self.frm_fuzz = tk.Frame(lf, bg="#ffffff")
        self.frm_fuzz.pack(anchor="w", pady=4)

        ttk.Separator(lf).pack(fill="x", pady=6)

        # ── FIRING STRENGTH ───────────────────────
        tk.Label(lf, text="Firing Strength (α) per Rule",
                 font=("Segoe UI", 9, "bold"), bg="#ffffff", fg="#1e293b"
                 ).pack(anchor="w")
        self.frm_alpha = tk.Frame(lf, bg="#ffffff")
        self.frm_alpha.pack(anchor="w", pady=4)

        ttk.Separator(lf).pack(fill="x", pady=6)

        # ── TABEL 10 DATA UJI ─────────────────────
        tk.Label(lf, text="10 Data Uji (Klik untuk Coba)",
                 font=("Segoe UI", 9, "bold"), bg="#ffffff", fg="#1e293b"
                 ).pack(anchor="w")
        tbl_wrap = tk.Frame(lf, bg="#ffffff")
        tbl_wrap.pack(fill="x", pady=4)

        cols = ("No", "Suhu", "Lembap", "Durasi")
        self.tree = ttk.Treeview(tbl_wrap, columns=cols, show="headings", height=8)
        for c, w in zip(cols, [28, 56, 56, 68]):
            self.tree.heading(c, text=c)
            self.tree.column(c, width=w, anchor="center")
        vsb = ttk.Scrollbar(tbl_wrap, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side="left", fill="x", expand=True)
        vsb.pack(side="left", fill="y")
        self.tree.bind("<<TreeviewSelect>>", self._on_tree_select)
        self._isi_tabel()

    # ── Panel Kanan: Notebook Tab Grafik ──────────
    def _build_right(self, parent):
        right = tk.Frame(parent, bg="#ffffff", relief="groove", bd=1)
        right.pack(side="left", fill="both", expand=True)

        self.nb = ttk.Notebook(right)
        self.nb.pack(fill="both", expand=True)

        # Konfigurasi tab: (Judul Tab, Saran Nama File, Fungsi Render)
        tabs_cfg = [
            ("Membership Function", "gui_membership.png", self._draw_mf),
            ("Implikasi Tiap Rule",  "gui_implikasi.png",  self._draw_impl),
            ("Agregasi & Defuzz",    "gui_agregasi.png",   self._draw_agg),
            ("Rule Viewer (α)",      "gui_ruleviewer.png", self._draw_rv),
        ]

        self.figures     = {}
        self.canvases    = {}
        self.tab_titles  = {}
        self.default_filenames = {}

        for idx, (label, default_fn, draw_fn) in enumerate(tabs_cfg):
            frm = tk.Frame(self.nb, bg="white")
            self.nb.add(frm, text=f"  {label}  ")

            self.tab_titles[idx] = label
            self.default_filenames[idx] = default_fn

            # Buat figure Matplotlib
            fig, axs = draw_fn(init=True)
            canvas = FigureCanvasTkAgg(fig, master=frm)
            canvas.get_tk_widget().pack(fill="both", expand=True)

            # Bar bawah: tombol simpan gambar dengan custom file explorer
            bar = tk.Frame(frm, bg="#f1f5f9", pady=6, padx=10)
            bar.pack(fill="x", side="bottom")

            lbl_info = tk.Label(bar,
                                text="📁 Ekspor grafik ke file gambar (PNG, JPG, PDF) ke folder pilihan Anda",
                                font=("Segoe UI", 8), bg="#f1f5f9", fg="#64748b")
            lbl_info.pack(side="left")

            btn_save = ttk.Button(
                bar,
                text="💾  Simpan Gambar (Pilih Lokasi...)",
                command=lambda i=idx: self._simpan_gambar_custom(i)
            )
            btn_save.pack(side="right")

            self.figures[idx]  = (fig, axs, draw_fn)
            self.canvases[idx] = canvas

    # ── Sinkronisasi Slider -> Entry & Hitung ──────
    def _on_slider_suhu(self, val):
        if self._sync_lock:
            return
        self._sync_lock = True
        fval = float(val)
        self.ent_suhu.delete(0, tk.END)
        self.ent_suhu.insert(0, f"{fval:.1f}")
        self._sync_lock = False
        self._hitung(from_entry=False)

    def _on_slider_kel(self, val):
        if self._sync_lock:
            return
        self._sync_lock = True
        fval = float(val)
        self.ent_kel.delete(0, tk.END)
        self.ent_kel.insert(0, f"{fval:.1f}")
        self._sync_lock = False
        self._hitung(from_entry=False)

    # ── Sinkronisasi Entry -> Slider & Hitung ──────
    def _on_entry_changed(self, source):
        if self._sync_lock:
            return
        try:
            if source == "suhu":
                val = float(self.ent_suhu.get().replace(",", "."))
                if not (15.0 <= val <= 40.0):
                    messagebox.showerror("Batas Nilai", "Suhu harus berada pada rentang 15 – 40 °C.")
                    return
                self._sync_lock = True
                self.slider_suhu.set(val)
                self._sync_lock = False
            elif source == "kel":
                val = float(self.ent_kel.get().replace(",", "."))
                if not (0.0 <= val <= 100.0):
                    messagebox.showerror("Batas Nilai", "Kelembapan harus berada pada rentang 0 – 100 %.")
                    return
                self._sync_lock = True
                self.slider_kel.set(val)
                self._sync_lock = False
        except ValueError:
            messagebox.showerror("Input Tidak Valid", "Silakan masukkan angka numerik yang benar.")
            return

        self._hitung(from_entry=True)

    # ── Pilihan dari Tabel Data Uji ────────────────
    def _on_tree_select(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        item = self.tree.item(sel[0])
        _, s_val, k_val, _ = item["values"]
        self._sync_lock = True
        self.ent_suhu.delete(0, tk.END)
        self.ent_suhu.insert(0, str(s_val))
        self.slider_suhu.set(float(s_val))

        self.ent_kel.delete(0, tk.END)
        self.ent_kel.insert(0, str(k_val))
        self.slider_kel.set(float(k_val))
        self._sync_lock = False

        self._hitung(from_entry=True)

    # ── Eksekusi Perhitungan & Render Grafik ───────
    def _hitung(self, from_entry=True):
        try:
            ns = float(self.ent_suhu.get().replace(",", "."))
            nk = float(self.ent_kel.get().replace(",", "."))
        except ValueError:
            if from_entry:
                messagebox.showerror("Input Salah", "Masukkan angka yang valid pada kotak input.")
            return

        if not (15.0 <= ns <= 40.0):
            if from_entry:
                messagebox.showerror("Input Salah", "Suhu harus berada antara 15 – 40 °C.")
            return
        if not (0.0 <= nk <= 100.0):
            if from_entry:
                messagebox.showerror("Input Salah", "Kelembapan harus berada antara 0 – 100 %.")
            return

        mu_s, mu_k, alpha_l, out_rule, agg, hasil = hitung_fis(ns, nk)
        self.result = (ns, nk, mu_s, mu_k, alpha_l, out_rule, agg, hasil)

        # Update tampilan hasil durasi
        self.lbl_hasil.config(text=f"{hasil:.2f} menit")
        if hasil < 10:
            kat = "Kategori: SINGKAT (< 10 menit)"
            color = "#0284c7"
        elif hasil < 20:
            kat = "Kategori: SEDANG (10 – 20 menit)"
            color = "#ea580c"
        else:
            kat = "Kategori: LAMA (> 20 menit)"
            color = "#16a34a"
        self.lbl_kat.config(text=kat, fg=color)

        # Update tabel Fuzzifikasi
        for w in self.frm_fuzz.winfo_children():
            w.destroy()
        hdrs = ["Variabel", "Himpunan", "μ"]
        for c, h in enumerate(hdrs):
            tk.Label(self.frm_fuzz, text=h, font=("Segoe UI", 8, "bold"),
                     bg="#ffffff", fg="#1e293b", padx=4).grid(row=0, column=c, sticky="w")
        row = 1
        for k, v in mu_s.items():
            fg = "#16a34a" if v > 0.001 else "#94a3b8"
            tk.Label(self.frm_fuzz, text="Suhu",  font=("Segoe UI", 8), bg="#ffffff", fg="#64748b"
                     ).grid(row=row, column=0, sticky="w", padx=4)
            tk.Label(self.frm_fuzz, text=k,       font=("Segoe UI", 8), bg="#ffffff", fg="#334155"
                     ).grid(row=row, column=1, sticky="w", padx=4)
            tk.Label(self.frm_fuzz, text=f"{v:.4f}", font=("Consolas", 8, "bold" if v > 0.001 else "normal"),
                     bg="#ffffff", fg=fg).grid(row=row, column=2, sticky="w", padx=4)
            row += 1
        for k, v in mu_k.items():
            fg = "#16a34a" if v > 0.001 else "#94a3b8"
            tk.Label(self.frm_fuzz, text="Lembap", font=("Segoe UI", 8), bg="#ffffff", fg="#64748b"
                     ).grid(row=row, column=0, sticky="w", padx=4)
            tk.Label(self.frm_fuzz, text=k,        font=("Segoe UI", 8), bg="#ffffff", fg="#334155"
                     ).grid(row=row, column=1, sticky="w", padx=4)
            tk.Label(self.frm_fuzz, text=f"{v:.4f}", font=("Consolas", 8, "bold" if v > 0.001 else "normal"),
                     bg="#ffffff", fg=fg).grid(row=row, column=2, sticky="w", padx=4)
            row += 1

        # Update tabel Firing Strength
        for w in self.frm_alpha.winfo_children():
            w.destroy()
        for c, h in enumerate(["Rule", "Kondisi", "α"]):
            tk.Label(self.frm_alpha, text=h, font=("Segoe UI", 8, "bold"),
                     bg="#ffffff", fg="#1e293b", padx=3).grid(row=0, column=c, sticky="w")
        for i, (a, b, c) in enumerate(RULE):
            fg = "#16a34a" if alpha_l[i] > 0.001 else "#94a3b8"
            tk.Label(self.frm_alpha, text=f"R{i+1}", font=("Consolas", 8, "bold" if alpha_l[i] > 0.001 else "normal"),
                     bg="#ffffff", fg="#334155").grid(row=i+1, column=0, sticky="w", padx=3)
            tk.Label(self.frm_alpha, text=f"{a} & {b}", font=("Segoe UI", 8),
                     bg="#ffffff", fg="#64748b").grid(row=i+1, column=1, sticky="w", padx=3)
            tk.Label(self.frm_alpha, text=f"{alpha_l[i]:.3f}",
                     font=("Consolas", 8, "bold" if alpha_l[i] > 0.001 else "normal"),
                     bg="#ffffff", fg=fg).grid(row=i+1, column=2, sticky="w", padx=3)

        # Update scrollregion agar seluruh rule (R1 - R9) dan data uji bisa di-scroll sampai bawah
        if hasattr(self, 'scrollable_frame') and hasattr(self, 'canvas_left'):
            self.scrollable_frame.update_idletasks()
            self.canvas_left.configure(scrollregion=self.canvas_left.bbox("all"))

        # Update semua grafik
        for idx, (fig, axs, draw_fn) in self.figures.items():
            draw_fn(fig=fig, axs=axs, data=self.result)
            self.canvases[idx].draw_idle()

    # ── Simpan Gambar dengan File Explorer Bebas ──
    def _simpan_gambar_custom(self, idx):
        if self.result is None:
            messagebox.showinfo("Informasi", "Silakan lakukan perhitungan terlebih dahulu.")
            return

        default_file = self.default_filenames[idx]
        title_tab = self.tab_titles[idx]
        initial_dir = self.last_save_dir if os.path.exists(self.last_save_dir) else os.path.abspath("hasil")

        # Buka dialog File Explorer untuk memilih folder dan nama file
        fpath = filedialog.asksaveasfilename(
            parent=self,
            title=f"Simpan Grafik [{title_tab}] — Pilih Lokasi",
            initialdir=initial_dir,
            initialfile=default_file,
            defaultextension=".png",
            filetypes=[
                ("PNG Image (*.png)", "*.png"),
                ("JPEG Image (*.jpg;*.jpeg)", "*.jpg;*.jpeg"),
                ("PDF Document (*.pdf)", "*.pdf"),
                ("Semua File (*.*)", "*.*")
            ]
        )

        # Jika user membatalkan dialog
        if not fpath:
            return

        # Catat direktori folder terakhir agar dialog tab berikutnya langsung buka folder ini
        self.last_save_dir = os.path.dirname(os.path.abspath(fpath))

        fig, _, _ = self.figures[idx]
        try:
            fig.savefig(fpath, dpi=160, bbox_inches="tight")
            messagebox.showinfo(
                "Berhasil Disimpan",
                f"Grafik '{title_tab}' berhasil disimpan ke:\n\n{os.path.normpath(fpath)}"
            )
        except Exception as err:
            messagebox.showerror("Gagal Menyimpan", f"Terjadi kesalahan saat menyimpan file:\n{err}")

    # ── Simpan Semua Bagian Terpisah Menjadi File .PNG ─
    def _simpan_semua_bagian_terpisah(self):
        if self.result is None:
            messagebox.showinfo("Informasi", "Silakan lakukan perhitungan terlebih dahulu.")
            return

        ns, nk = self.result[0], self.result[1]
        initial_dir = self.last_save_dir if os.path.exists(self.last_save_dir) else os.path.abspath("hasil")

        # Buka dialog File Explorer untuk memilih folder tujuan penyimpanan
        target_dir = filedialog.askdirectory(
            parent=self,
            title="Pilih Folder untuk Menyimpan Gambar Setiap Bagian (.PNG)",
            initialdir=initial_dir
        )

        if not target_dir:
            return

        # Catat folder terakhir agar dialog berikutnya langsung membuka folder ini
        self.last_save_dir = target_dir

        # 4 Bagian grafik yang disimpan secara terpisah ke file .png
        files_to_save = [
            (0, f"01_membership_function_suhu{int(ns)}_kel{int(nk)}.png", "Membership Function"),
            (1, f"02_implikasi_tiap_rule_suhu{int(ns)}_kel{int(nk)}.png",  "Implikasi Tiap Rule"),
            (2, f"03_agregasi_dan_defuzz_suhu{int(ns)}_kel{int(nk)}.png",   "Agregasi & Defuzzifikasi"),
            (3, f"04_rule_viewer_alpha_suhu{int(ns)}_kel{int(nk)}.png",    "Rule Viewer (Firing Strength)"),
        ]

        saved_files = []
        try:
            for idx, filename, label in files_to_save:
                fig, _, _ = self.figures[idx]
                out_path = os.path.join(target_dir, filename)
                fig.savefig(out_path, dpi=180, bbox_inches="tight")
                saved_files.append(filename)

            msg = (
                f"Berhasil menyimpan 4 file gambar bagian secara terpisah ke folder:\n\n"
                f"{os.path.normpath(target_dir)}\n\n"
                f"Daftar file tersimpan (.PNG):\n" +
                "\n".join([f"  ✓ {f}" for f in saved_files])
            )
            messagebox.showinfo("Berhasil Disimpan", msg)
        except Exception as err:
            messagebox.showerror("Gagal Menyimpan", f"Terjadi kesalahan saat menyimpan file gambar:\n{err}")

    # ── Isi Tabel 10 Data Uji ──────────────────────
    def _isi_tabel(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for no, (s, k) in enumerate(DATA_UJI, 1):
            dur = hitung_fis(s, k)[-1]
            tag = "alt" if no % 2 == 0 else ""
            self.tree.insert("", "end",
                             values=(no, s, k, f"{dur:.2f}"),
                             tags=(tag,))
        self.tree.tag_configure("alt", background="#f8fafc")

    # ═══════════════════════════════════════════════
    # FUNGSI GAMBAR PER TAB
    # ═══════════════════════════════════════════════

    # ── Tab 1: Membership Function ─────────────────
    def _draw_mf(self, init=False, fig=None, axs=None, data=None):
        if init:
            fig = Figure(figsize=(8, 3.6), facecolor="white", tight_layout=True)
            axs = [fig.add_subplot(1, 3, i+1) for i in range(3)]
            color_sets = [
                [("DINGIN","#2563eb"), ("NORMAL","#16a34a"), ("PANAS","#dc2626")],
                [("KERING","#ea580c"), ("LEMBAP","#0284c7"), ("BASAH","#9333ea")],
                [("SINGKAT","#dc2626"),("SEDANG","#ea580c"), ("LAMA","#16a34a")],
            ]
            data_static = [
                (suhu,       mf_suhu,       "Suhu Udara (°C)"),
                (kelembapan, mf_kelembapan, "Kelembapan Tanah (%)"),
                (durasi,     mf_durasi,     "Durasi Penyiraman (mnt)"),
            ]
            for ax, (x, mf, lbl), cs in zip(axs, data_static, color_sets):
                for (nama, _), (_, col) in zip(mf.items(), cs):
                    ax.plot(x, mf[nama], color=col, linewidth=1.8, label=nama)
                    ax.fill_between(x, mf[nama], alpha=0.08, color=col)
                ax.set_title(f"MF {lbl}", fontsize=9, fontweight="bold", color="#1e293b")
                ax.set_xlabel(lbl, fontsize=8)
                ax.set_ylabel("μ (Derajat)", fontsize=8)
                ax.legend(fontsize=7, loc="upper right")
                ax.grid(True, alpha=0.3, linestyle="--")
                ax.set_ylim(-0.05, 1.1)

            # Garis vertikal posisi input
            for ax in axs[:2]:
                ax._vline = ax.axvline(0, color="#1e293b", linestyle="--",
                                        linewidth=1.4, alpha=0, label="Input")
            return fig, axs

        ns, nk = data[0], data[1]
        for idx_ax, ax in enumerate(axs[:2]):
            val = ns if idx_ax == 0 else nk
            lbl = f"Input={val:.1f}°C" if idx_ax == 0 else f"Input={val:.1f}%"
            for line in ax.lines:
                if line.get_linestyle() == "--":
                    line.set_alpha(1)
                    line.set_xdata([val, val])
                    line.set_label(lbl)
            ax.legend(fontsize=7, loc="upper right")
        return fig, axs

    # ── Tab 2: Implikasi Tiap Rule ─────────────────
    def _draw_impl(self, init=False, fig=None, axs=None, data=None):
        if init:
            fig = Figure(figsize=(8, 5.2), facecolor="white")
            fig.subplots_adjust(left=0.07, right=0.97, top=0.91,
                                bottom=0.07, wspace=0.35, hspace=0.55)
            axs = [fig.add_subplot(3, 3, i+1) for i in range(9)]
            for ax in axs:
                ax.set_xlim(0, 30)
                ax.set_ylim(-0.05, 1.1)
                ax.grid(True, alpha=0.3, linestyle="--")
            fig.suptitle("Implikasi (MIN) Setiap Rule terhadap Output Durasi",
                         fontsize=10, fontweight="bold", color="#1e293b")
            return fig, axs

        alpha_l, out_rule = data[4], data[5]
        for i, ax in enumerate(axs):
            ax.cla()
            a, b, c = RULE[i]
            val_a = alpha_l[i]
            fill_col = "#2563eb" if val_a > 0.001 else "#cbd5e1"
            line_col = "#1d4ed8" if val_a > 0.001 else "#94a3b8"

            ax.fill_between(durasi, out_rule[i], alpha=0.35, color=fill_col)
            ax.plot(durasi, out_rule[i], color=line_col, linewidth=1.4)
            ax.set_title(f"R{i+1}: {a} ∧ {b} → {c}\nα = {val_a:.3f}",
                         fontsize=7.5, pad=3,
                         color="#0f172a" if val_a > 0.001 else "#64748b",
                         fontweight="bold" if val_a > 0.001 else "normal")
            ax.set_ylim(-0.05, 1.1)
            ax.grid(True, alpha=0.3, linestyle="--")
        fig.suptitle("Implikasi (MIN) Setiap Rule terhadap Output Durasi",
                     fontsize=10, fontweight="bold", color="#1e293b")
        return fig, axs

    # ── Tab 3: Agregasi & Defuzzifikasi ───────────
    def _draw_agg(self, init=False, fig=None, axs=None, data=None):
        if init:
            fig = Figure(figsize=(8, 3.6), facecolor="white", tight_layout=True)
            axs = fig.add_subplot(1, 1, 1)
            axs.set_xlim(0, 30)
            axs.set_ylim(-0.05, 1.15)
            axs.grid(True, alpha=0.3, linestyle="--")
            axs.set_title("Agregasi (MAX) dan Defuzzifikasi (Centroid)",
                          fontsize=10, fontweight="bold", color="#1e293b")
            axs.set_xlabel("Durasi Penyiraman (menit)", fontsize=9)
            axs.set_ylabel("Derajat Keanggotaan Agregasi", fontsize=9)
            return fig, axs

        agg, hasil = data[6], data[7]
        axs.cla()
        axs.fill_between(durasi, agg, alpha=0.35, color="#16a34a", label="Area Agregasi (MAX)")
        axs.plot(durasi, agg, color="#15803d", linewidth=2)
        axs.axvline(hasil, color="#dc2626", linestyle="--", linewidth=2,
                    label=f"Centroid = {hasil:.2f} menit")
        axs.set_title("Agregasi (MAX) dan Defuzzifikasi (Centroid)",
                      fontsize=10, fontweight="bold", color="#1e293b")
        axs.set_xlabel("Durasi Penyiraman (menit)", fontsize=9)
        axs.set_ylabel("Derajat Keanggotaan Agregasi", fontsize=9)
        axs.set_ylim(-0.05, 1.15)
        axs.legend(fontsize=9, loc="upper right")
        axs.grid(True, alpha=0.3, linestyle="--")
        return fig, axs

    # ── Tab 4: Rule Viewer ─────────────────────────
    def _draw_rv(self, init=False, fig=None, axs=None, data=None):
        if init:
            fig = Figure(figsize=(8, 3.6), facecolor="white", tight_layout=True)
            axs = fig.add_subplot(1, 1, 1)
            axs.set_ylim(0, 1.25)
            axs.grid(True, alpha=0.3, axis="y", linestyle="--")
            axs.set_title("Rule Viewer — Firing Strength (α)",
                          fontsize=10, fontweight="bold", color="#1e293b")
            axs.set_xlabel("Aturan (Rule)", fontsize=9)
            axs.set_ylabel("Firing Strength (α)", fontsize=9)
            return fig, axs

        alpha_l = data[4]
        axs.cla()
        labels = [f"R{i+1}" for i in range(9)]
        colors = ["#16a34a" if v > 0.001 else "#cbd5e1" for v in alpha_l]
        bars = axs.bar(labels, alpha_l, color=colors, edgecolor="#475569", linewidth=0.7)

        for bar, val in zip(bars, alpha_l):
            if val > 0.001:
                axs.text(bar.get_x() + bar.get_width()/2,
                         bar.get_height() + 0.02,
                         f"{val:.3f}", ha="center", va="bottom",
                         fontsize=8, fontweight="bold", color="#15803d")

        # Kotak legenda deskripsi aturan
        rule_txt = "\n".join(
            [f"R{i+1}: IF {a} AND {b} THEN {c}" for i, (a, b, c) in enumerate(RULE)])
        axs.text(1.01, 1.0, rule_txt, transform=axs.transAxes,
                 fontsize=7.5, va="top", ha="left", fontfamily="Consolas",
                 bbox=dict(facecolor="#f8fafc", edgecolor="#cbd5e1",
                           boxstyle="round,pad=0.5"))

        axs.set_title("Rule Viewer — Firing Strength (α)",
                      fontsize=10, fontweight="bold", color="#1e293b")
        axs.set_xlabel("Aturan (Rule)", fontsize=9)
        axs.set_ylabel("Firing Strength (α)", fontsize=9)
        axs.set_ylim(0, 1.25)
        axs.grid(True, alpha=0.3, axis="y", linestyle="--")
        return fig, axs


# ───────────────────────────────────────────────────
if __name__ == "__main__":
    app = App()
    app.mainloop()
