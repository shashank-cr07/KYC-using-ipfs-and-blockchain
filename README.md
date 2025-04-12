# KYC using IPFS and Blockchain

This project uses OCR, Streamlit, and blockchain integration to perform KYC (Know Your Customer) verification, leveraging IPFS and various modern technologies.

---

## Setup Instructions (Linux)

### 1. Create and Activate a Virtual Environment(Suggested)

```bash
python3 -m venv myenv
source myenv/bin/activate
```

### 2. Upgrade pip if needed 
```bash
pip install --upgrade pip
```

### 3.Install python dependancies
```bash
pip install \
  streamlit \
  opencv-python-headless \
  numpy \
  pytesseract \
  twilio \
  pillow \
  requests \
  selenium \
  webdriver-manager
```
### 4. Install system dependancies
#### a. Install tersseract
```bash
sudo apt install tesseract-ocr
```
#### b. Install chrome on linux (Suggested
```bash
sudo apt install google-chrome-stable
```
Use the below if chrome-stable (above) is unavailable
```bash
sudo apt install chromium-browser

```
