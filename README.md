# 🔮 BurnoutCheck — Sistem Fuzzy Risiko Burnout Mahasiswa

Sistem penilaian risiko burnout mahasiswa berbasis **Logika Fuzzy Mamdani** dengan antarmuka web statis.

---

## 🧠 Tentang Sistem

BurnoutCheck menggunakan metode **Fuzzy Mamdani** untuk mendeteksi dini risiko burnout akademik mahasiswa berdasarkan 4 variabel input.

### Variabel Input

| Variabel | Himpunan Fuzzy |
|---|---|
| 📚 Beban Akademik | Rendah / Sedang / Tinggi |
| 😴 Kualitas Tidur | Buruk / Sedang / Baik |
| 🤝 Dukungan Sosial | Minim / Sedang / Besar |
| ⏰ Tekanan Waktu | Longgar / Sedang / Ketat |

### Variabel Output

| Variabel | Himpunan Fuzzy |
|---|---|
| 🎯 Risiko Burnout | Sangat Rendah / Rendah / Sedang / Tinggi / Sangat Tinggi |

### Fungsi Keanggotaan

- Input menggunakan fungsi **Trapesium** dan **Segitiga**
- Output menggunakan fungsi **Trapesium**
- Defuzzifikasi menggunakan metode **Centroid**
- Total **27 rules** Mamdani

---

## 📁 Struktur Proyek

```
sistem_fuzzy/
├── fuzzy_burnout.py   # Logika fuzzy (scikit-fuzzy)
├── server.py          # Web server Python sederhana
└── static/
    └── index.html     # Antarmuka web
```

---

## ⚙️ Instalasi & Menjalankan

### 1. Clone repository

```bash
git clone https://github.com/username/burnout-fuzzy.git
cd sistem_fuzzy
```

### 2. Install dependencies

```bash
pip install numpy scikit-fuzzy matplotlib
```

### 3. Jalankan server

```bash
cd burnout_fuzzy
python server.py
```

### 4. Buka browser

```
http://localhost:8080
```

> ⚠️ Pastikan menjalankan `server.py` dari dalam folder `sistem_fuzzy`, bukan dari luar.

---

## 🛠️ Teknologi

| Komponen | Teknologi |
|---|---|
| Logika Fuzzy | Python, scikit-fuzzy |
| Visualisasi | Matplotlib |
| Web Server | Python `http.server` |
| Frontend | HTML, CSS, JavaScript |

---

## 📊 Cara Kerja

1. Pengguna menggeser 4 slider sesuai kondisi aktual
2. Nilai dikirim ke backend Python via HTTP GET
3. Sistem fuzzy Mamdani memproses input sesuai 27 rules
4. Hasil defuzzifikasi dikembalikan beserta grafik fungsi keanggotaan
5. Antarmuka menampilkan label risiko, nilai fuzzy, dan saran

---