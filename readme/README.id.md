<p align="center"><a href="../README.md">
  <img src="../assets/logo.png" alt="TokenMix Bulk Creator" width="150">
</a></p>

<p align="center"><img src="../assets/banner.png" alt="TokenMix Bulk Creator banner"></p>

<p align="center">
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"></a>
  <a href="https://playwright.dev/"><img src="https://img.shields.io/badge/playwright-%E2%9C%94-2EAD33?style=for-the-badge&logo=playwright&logoColor=white" alt="Playwright"></a>
  <a href="../LICENSE"><img src="https://img.shields.io/badge/license-MIT-22e6a5?style=for-the-badge" alt="MIT License"></a>
  <img src="https://img.shields.io/badge/platform-linux%20%7C%20macos%20%7C%20windows-7c5cff?style=for-the-badge" alt="Platform">
</p>

# TokenMix Bulk Account & API Key Creator (Bahasa Indonesia)

> Pembuat akun TokenMix massal otomatis dengan disposable inbox ([cilaaa.my.id](https://cilaaa.my.id/)) dan pembuatan API key otomatis (`sk-tm-...`).

<p><a href="../README.md">English</a> · <strong>Indonesia</strong></p>

---

`tokenmix-bulk` mengintegrasikan pembuatan email sementara ([cilaaa.my.id](https://cilaaa.my.id/) / [temp-mail.io](https://temp-mail.io)), penyelesaian tantangan Cloudflare Turnstile secara otomatis berbasis Playwright stealth, serta pembuatan API Key TokenMix secara instan dalam satu alur eksekusi.

---

## 🚀 Fitur Utama

- **⚡ Integrasi Cepat [cilaaa.my.id](https://cilaaa.my.id/)**: Pembuatan inbox instan dan pengambilan kode OTP langsung via REST API tanpa antri.
- **🛡️ Bypass Cloudflare Turnstile Otomatis**: Menyelesaikan verifikasi Turnstile dalam **~4-5 detik** menggunakan Playwright browser stealth.
- **🔑 Auto Generate API Key**: Otomatis membuat API key siap pakai (contoh: `relay-prime-summit-vsm3`).
- **💾 Penyimpanan Aman Bertahap**: Data akun langsung disimpan ke `accounts.json` dan `accounts.csv` seketika setelah dibuat.
- **⚙️ Konkurensi & Retry Otomatis**: Mendukung banyak worker paralel dan otomatis mencoba ulang jika gagal.

---

## 📋 Persyaratan Sistem

- **Python 3.9+**
- **Git**
- **Chromium** (terinstal lewat Playwright)

---

## 📦 Panduan Instalasi & Pemasangan

### 1. Clone Repository
```bash
git clone https://github.com/itscasaa/tokenmix-bulk.git
cd tokenmix-bulk
```

### 2. Buat & Aktifkan Virtual Environment
**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependensi & Browser Playwright
```bash
pip install -e .
playwright install chromium
```

---

## ⚡ Cara Menjalankan

### 1. Buat 1 Akun (Browser Terbuka / Visible)
```bash
python -m tokenmix_bulk -n 1 --mail-provider cilaaa
```

### 2. Buat Banyak Akun di Background (Headless)
```bash
python -m tokenmix_bulk -n 5 --headless --mail-provider cilaaa
```

### 3. Buat dengan Mode Paralel (Concurrency)
```bash
python -m tokenmix_bulk -n 10 -c 2 --headless
```

### 4. Menggunakan File Konfigurasi
```bash
python -m tokenmix_bulk --config config.example.json
```

---

## 🛠️ Referensi Parameter CLI

| Flag | Default | Keterangan |
| --- | --- | --- |
| `-n, --count` | `1` | Jumlah akun yang ingin dibuat |
| `-c, --concurrency` | `1` | Jumlah worker browser paralel |
| `-o, --output` | `accounts.json` | Path file keluaran JSON |
| `--csv` | `accounts.csv` | Path file keluaran CSV |
| `--mail-provider` | `cilaaa` | Provider email (`cilaaa`, `temp-mail-io`, `mail-tm`) |
| `--key-prefix` | random | Prefix nama API key |
| `--headless` | `false` | Jalankan tanpa jendela browser |
| `--browser` | `chromium` | Browser engine (`chromium`, `firefox`, `webkit`) |
| `--config` | `None` | Path file config JSON/YAML |
| `--proxy` | `None` | URL Proxy (contoh: `http://user:pass@host:port`) |
| `-v, --verbose` | `false` | Tampilkan detail debug log |

---

## 📄 Lisensi

Didistribusikan di bawah [MIT License](../LICENSE).
