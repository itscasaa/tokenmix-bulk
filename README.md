<p align="center"><a href="README.md">
  <img src="assets/logo.png" alt="TokenMix Bulk Creator" width="150">
</a></p>

<p align="center"><img src="assets/banner.png" alt="TokenMix Bulk Creator banner"></p>

<p align="center">
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"></a>
  <a href="https://playwright.dev/"><img src="https://img.shields.io/badge/playwright-%E2%9C%94-2EAD33?style=for-the-badge&logo=playwright&logoColor=white" alt="Playwright"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-22e6a5?style=for-the-badge" alt="MIT License"></a>
  <img src="https://img.shields.io/badge/platform-linux%20%7C%20macos%20%7C%20windows-7c5cff?style=for-the-badge" alt="Platform">
</p>

# TokenMix Bulk Account & API Key Creator

> Bulk-provision TokenMix accounts with disposable inboxes ([cilaaa.my.id](https://cilaaa.my.id/)) and auto-generate OpenAI-compatible API keys (`sk-tm-...`).

<p><strong>English</strong> · <a href="readme/README.id.md">Indonesia</a></p>

---

`tokenmix-bulk` combines automated disposable mailboxes ([cilaaa.my.id](https://cilaaa.my.id/) / [temp-mail.io](https://temp-mail.io)), a stealth browser context that clears Cloudflare Turnstile challenges, and the TokenMix REST API into a seamless, high-speed provisioning pipeline.

---

## 🚀 Features

- **⚡ Fast Mailbox Integration**: Uses [cilaaa.my.id](https://cilaaa.my.id/) (CasaTemp) REST API for instantaneous mailbox generation and OTP extraction.
- **🛡️ Turnstile Auto-Solver**: Injects and solves Cloudflare Turnstile invisible challenges with Playwright stealth in ~4-5 seconds.
- **🔑 Auto API Keys**: Automatically generates named API keys (e.g. `relay-prime-summit-vsm3`).
- **💾 Crash-Safe Incremental Output**: Appends each created account to `accounts.json` and `accounts.csv` immediately.
- **⚙️ Concurrency & Retries**: Supports multiple parallel workers and auto-retries on failed attempts.
- **🎛️ Provider Agnostic**: Supports `cilaaa` (default), `temp-mail-io`, and `mail-tm`.

---

## 📋 Requirements

- **Python 3.9+**
- **Git**
- **Chromium** (installed via Playwright)

---

## 📦 Installation & Setup

### 1. Clone Repository
```bash
git clone https://github.com/itscasaa/tokenmix-bulk.git
cd tokenmix-bulk
```

### 2. Create and Activate Virtual Environment
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

### 3. Install Dependencies & Playwright
```bash
pip install -e .
playwright install chromium
```

---

## ⚡ Quick Start

### 1. Run 1 Account (Visible Browser)
```bash
python -m tokenmix_bulk -n 1 --mail-provider cilaaa
```

### 2. Run Batch in Background (Headless)
```bash
python -m tokenmix_bulk -n 5 --headless --mail-provider cilaaa
```

### 3. Run with Concurrency
```bash
python -m tokenmix_bulk -n 10 -c 2 --headless
```

### 4. Run via Configuration File
```bash
python -m tokenmix_bulk --config config.example.json
```

---

## 🛠️ CLI Reference

| Flag | Default | Description |
| --- | --- | --- |
| `-n, --count` | `1` | Number of accounts to create |
| `-c, --concurrency` | `1` | Parallel worker count |
| `-o, --output` | `accounts.json` | JSON output file path |
| `--csv` | `accounts.csv` | CSV output file path |
| `--mail-provider` | `cilaaa` | Mail provider (`cilaaa`, `temp-mail-io`, `mail-tm`) |
| `--key-prefix` | random | Prefix for generated API key names |
| `--headless` | `false` | Run browser in background without GUI |
| `--browser` | `chromium` | Browser engine (`chromium`, `firefox`, `webkit`) |
| `--config` | `None` | Path to JSON/YAML config file |
| `--proxy` | `None` | HTTP/SOCKS5 proxy (e.g. `http://user:pass@host:port`) |
| `-v, --verbose` | `false` | Enable verbose debug logging |

---

## 📊 Output Format

### `accounts.json`
```json
{
  "total": 1,
  "succeeded": 1,
  "failed": 0,
  "accounts": [
    {
      "index": 1,
      "email": "ember.comet@cilaaa.my.id",
      "password": "Password123!",
      "username": "ember.comet",
      "api_key": "sk-tm-toqapRGKvlrZbeTLdJjNdYGDY9JV1jSyGCrepdFZmk3iAtBT",
      "api_key_name": "relay-prime-summit-vsm3",
      "key_id": "12345",
      "balance": "$0.0000",
      "status": "success",
      "attempts": 1
    }
  ]
}
```

---

## 📄 License

Distributed under the [MIT License](LICENSE).
