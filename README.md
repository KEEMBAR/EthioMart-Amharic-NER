# EthioMart-Amharic-NER

## Project Overview

EthioMart-Amharic-NER is a data science project focused on building a Named Entity Recognition (NER) system for Amharic-language e-commerce data collected from Telegram channels. The goal is to extract key business entities (products, prices, locations, etc.) from unstructured messages to power a centralized e-commerce platform for Ethiopia.

## Business Need

With the rise of Telegram-based e-commerce in Ethiopia, vendors and customers face challenges due to decentralized channels. EthioMart aims to consolidate real-time data from multiple Telegram channels, enabling seamless product discovery and analytics. This project supports that vision by providing structured, machine-readable data through NER.

## Folder Structure

```
EthioMart-Amharic-NER/
│
├── data/                # Raw and processed data (not tracked by git, managed by DVC)
│   ├── raw/             # Unprocessed, original data from Telegram
│   ├── processed/       # Cleaned, tokenized, and labeled data
│
├── scripts/             # Python scripts for scraping, preprocessing, etc.
├── notebooks/           # Jupyter notebooks for EDA, labeling, and analysis
├── models/              # Saved and fine-tuned model files
├── reports/             # Interim and final PDF reports
├── requirements.txt     # Python dependencies
├── .gitignore           # Files/folders to ignore in git
├── .dvc/                # DVC configuration and cache
├── data.dvc             # DVC tracking file for data/
└── README.md            # Project overview and instructions
```

## Task 1: Data Collection, Preprocessing, and EDA

- **Data Ingestion:** Messages are scraped from five major Ethiopian e-commerce Telegram channels using a custom Python script (`scripts/telegram_scraper.py`).
- **Preprocessing:** Raw messages are cleaned (removal of URLs, emojis, symbols, etc.), normalized, and tokenized. Processed data is saved as per-message JSON files in `data/processed/text/<channel>/`.
- **EDA:** Exploratory Data Analysis is performed in a Jupyter notebook (`notebooks/eda_processed_text.ipynb`) to check data quality and tokenization.

## Task 2: NER Labeling in CoNLL Format

- A subset of 30–50 messages is randomly sampled from the processed data.
- Each token is manually labeled with entity tags (e.g., `B-Product`, `I-Product`, `B-LOC`, `B-PRICE`, `O`, etc.) in a notebook (`notebooks/2_data_labeling.ipynb`).
- The labeled data is exported as a plain text file in CoNLL format (`data/processed/ner_labeled_sample.conll`) for model training.

## How to Run the Main Scripts

1. **Set up your environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. **Scrape Telegram data:**
   ```bash
   python scripts/telegram_scraper.py
   ```
3. **Preprocess text data:**
   ```bash
   python scripts/preprocess_text.py
   ```
4. **Perform EDA:**
   - Open `notebooks/eda_processed_text.ipynb` in Jupyter and run the cells.
5. **Label data for NER:**
   - Open `notebooks/2_data_labeling.ipynb` and follow the workflow to label and export data in CoNLL format.

## Data & Version Control

- **Data files** are managed with DVC and are not tracked by git.
- **Session files** and virtual environments are ignored via `.gitignore`.

## Next Steps

- Expand labeled dataset for improved NER model training.
- Fine-tune and evaluate transformer-based NER models.
- Apply model interpretability and analytics as outlined in the project plan.

---

For more details, see the interim and final reports in the `reports/` folder.
