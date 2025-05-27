# 🏨 PortusReviews – Hotel/Restaurant Review Intelligence App

**PortusReviews** is a powerful review-processing pipeline for hospitality businesses. It scans hotel/restaurant reviews from multiple sources, cleans and enriches the data, and generates high-quality reply drafts and sentiment analysis reports using AI.

---

## 🚀 Features

* **One‑click automation** with the `All In` button: runs scan → clean → reply → sentiment analysis across all configured hotels and review platforms.
* **Multi‑site scraping**: TripAdvisor, Google, Booking.com, Expedia.
* **Dynamic config system**:

  * Select jobs to run (`scan`, `clean`, `reply`, `sa`)
  * Toggle individual review sources on/off
  * Choose provider (`OpenAI`, `Google`, `xAI`)
* **Live editing**:

  * Input prompts, temperature, and other generation parameters
  * Cutoff dates, number of reviews, hotel URLs — all real-time editable
* **AI-powered generation**:

  * Response drafts tailored to the actual content of each review
  * Sentiment scores + full Word report

---

## 🛠 Tech Stack

* **Language:** Python
* **GUI Framework:** [Flet](https://flet.dev/)
* **AI Providers:** OpenAI, Google Gemini, xAI (via API)
* **Data Processing:** OpenPyXL, python-docx
* **Packaging:** PyInstaller (for `.exe` delivery)

---

## 🗂 Folder Structure

```
PortusScan/
│
├── portus_config_module/       # YAML config manager, live param access
├── portus_interface_gui_module/ # Flet GUI (top bar, actions, tabs, dialogs)
├── scan_module/                # Review site validator + Apify scan runner
├── clean_module/               # Column filtering logic
├── reply_module/               # AI reply generation per review
├── portus_sa_module/           # Sentiment analysis + DOCX report
├── writer_module/              # Output path manager
├── main.py                     # App launcher
├── review_app_config.yaml      # Full pipeline config
├── .env                        # Provider API keys
└── README.md                   # This file
```

---

## ⚙️ Setup

### 1. Clone the Repo

```bash
git clone https://github.com/yourorg/portus_scan.git
cd portus_scan
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Add API Keys

Rename `.env.example` to `.env` file in the root and replace the placeholders with your API keys:

```env
# AI provider API keys (replace placeholders with real keys)
OPENAI_API_KEY=your-api-key-goes-here
GEMINI_API_KEY=your-api-key-goes-here
XAI_API_KEY=your-api-key-goes-here
# Apify API key (replace placeholder with real keys)
APIFY_API_KEY=your-api-key-goes-here
```

### 4. Launch

```bash
python main.py
```

### 5. Optional: Build as EXE

```bash
pyinstaller --noconfirm --windowed --onefile main.py
```

---

## 🧠 Shortcuts

| Shortcut     | Action                         |
| ------------ | ------------------------------ |
| Ctrl+G       | Run full pipeline              |
| Ctrl+Shift+G | Run All In (multi‑hotel)       |
| Ctrl+N       | Focus review count             |
| Ctrl+D       | Focus cutoff date              |
| Ctrl+O       | Pick output folder             |
| Ctrl+A       | API Keys dialog                |
| Ctrl+,       | Settings dialog                |
| Ctrl+H       | Help dialog                    |
| Ctrl+1/2/3   | Switch provider (OpenAI, etc.) |

---

## 📊 Output

* **Cleaned Review Excel** (per site)
* **Generated Reply Drafts** (per review)
* **Sentiment Report (.docx)** with:

  * AI-generated sentiment analysis
  * Global score & summary
  * Review-by-review details
  * Embedded replies

---

## 👤 Credits

Developed by [PerceivingAI](https://x.com/PerceivingAI)
All components are open-source and modular.