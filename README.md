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

---

# Running The files :

## Things to change before running:
#### 1. Adding twillio and pinata api keys(After you create an account here) in Main_folder/blockchain-storage/pancard_model4.py
#### 2. Adding email and password in Main_folder/blockchain-storage/test4.py for https://apicentral.idfy.com/sessions/new (After you create an account here)
#### 3. Adding pinata api key in Main_folder/blockchain-storage/IPFS.py  

## Things to keep in mind before running
When running pancard_model4.py ensure chrome on linux is closed and everytime you upload a pan on this website it opens chrome.  
You will have to logout of https://apicentral.idfy.com/sessions/new everytime before or during the pan card execution.  
When the chrome opens for verification of valid pan from govt database just logout and do not click anything on chrom when it opens on its own.  

## Run on 4 seperate terminals 
### 0. Navigate on every terminal to the file:
```bash
cd Main_folder/blockchain-storage
```
### 1. Running the blockchain (Very important):
```bash
npx hardhat node
```
### 2. Running the main uploading pan card website:
```bash
streamlit run pancarad_model4.py
```
### 3. Running the bank verification of kycs using contract address website:
```bash
streamlit run bank2.py
```
### 4. Running the ipfs check to retrive pan card image for law enforcement:
```bash
streamlit run IPFS.py
```
