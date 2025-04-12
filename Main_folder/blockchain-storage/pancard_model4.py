import streamlit as st
import random
import cv2
import numpy as np
import pytesseract
import re
import json
import tempfile
import subprocess
from twilio.rest import Client
from PIL import Image
from test4 import verify_pan  # Import verify_pan from test4
import requests
import hashlib
import numpy as np
from PIL import Image
import os
import io
# Twilio Credentials (Use Environment Variables for Security)
# Set all of these using twillio 
ACCOUNT_SID = ""
AUTH_TOKEN = ""
FROM_NUMBER = ""
TO_NUMBER = ""  # you can set a custom to number i.e the owner of the aadhar but free version of twillio doesnt allow

#Set your pinata api key and secret key 
PINATA_API_KEY = ""
PINATA_SECRET_API_KEY = ""

# Streamlit UI Customization
st.set_page_config(page_title="PAN Verification System", layout="centered")

# Store session state variables
if "otp" not in st.session_state:
    st.session_state.otp = None
if "verified" not in st.session_state:
    st.session_state.verified = False
if "pan_verified" not in st.session_state:
    st.session_state.pan_verified = False
if "pan_number" not in st.session_state:
    st.session_state.pan_number = None
if "dob" not in st.session_state:
    st.session_state.dob = None
if "output" not in st.session_state:
    st.session_state.output = ""
if "online_verified" not in st.session_state:
    st.session_state.online_verified = False

# Function: Extract PAN Details
def extract_pan_details(image):
    text = pytesseract.image_to_string(image, config="--psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/")
    pan_number = re.findall(r"[A-Z]{5}[0-9]{4}[A-Z]", text)
    dob = re.findall(r"\d{2}/\d{2}/\d{4}", text)  # Extract DOB in DD/MM/YYYY format
    return pan_number[0] if pan_number else None, dob[0] if dob else None

# Function: Convert DOB to YYYY-MM-DD Format
def convert_date(dob):
    try:
        day, month, year = dob.split("/")
        return f"{year}-{month}-{day}"
    except:
        return None

# Function: Send OTP via Twilio
def send_otp():
    otp = random.randint(100000, 999999)
    st.session_state.otp = otp

    message_body = f"Hello, your PAN Verification OTP is: {otp}"

    try:
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        client.messages.create(
            body=message_body,
            from_=FROM_NUMBER,
            to=TO_NUMBER
        )
        st.success("✅ OTP sent successfully! Please check your phone.")
    except Exception as e:
        st.error("❌ Error sending OTP. Please try again.")
        print(str(e))

# 🌟 **Step 1: Upload PAN Card Image**
st.title("🔍 PAN Card Verification System")
uploaded_file = st.file_uploader("📤 Upload PAN Card Image", type=["png", "jpg", "jpeg"])

if uploaded_file and not st.session_state.pan_verified:
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(uploaded_file.getvalue())
        image_path = temp_file.name

    image = cv2.imread(image_path)

    # Extract PAN number and DOB
    pan_number, dob = extract_pan_details(image)

    if pan_number and dob:
        st.success(f"✅ PAN Number Detected: {pan_number}")
        st.success(f"📅 DOB Detected: {dob}")
        st.session_state.pan_number = pan_number
        st.session_state.dob = convert_date(dob)

        # **Step 2: Online PAN Verification using test4.verify_pan()**
        st.info("🔄 Verifying PAN online... Please wait.")
        result = verify_pan(pan_number, st.session_state.dob)

        if "error" in result:
            st.error(f"❌ Online verification failed: {result['error']}")
        else:
            try:
                response_json = json.loads(result.get("json_result", "{}"))
                ver_status = response_json[0].get("status", "").lower()

                if ver_status == "completed":
                    st.session_state.pan_verified = True
                    st.session_state.online_verified = True
                    st.success("✅ Online PAN verification successful!")
                else:
                    st.error("❌ PAN verification failed. Invalid details.")
            except Exception as e:
                st.error(f"❌ Error processing verification response: {str(e)}")

    else:
        st.error("❌ PAN Number or DOB could not be extracted. Try a clearer image.")

# 🌟 **Step 3: OTP Verification**
if st.session_state.pan_verified and st.session_state.online_verified and not st.session_state.verified:
    st.subheader("📲 OTP Verification")

    if st.button("📩 Send OTP"):
        send_otp()

    user_otp = st.text_input("🔢 Enter the OTP received:", "")

    if st.button("✅ Submit OTP"):
        if st.session_state.otp and str(user_otp) == str(st.session_state.otp):
            st.success("✅ OTP Verified Successfully!")
            st.session_state.verified = True
        else:
            st.error("❌ Invalid OTP. Please try again.")

# 🌟 **Step 4: Save Image and Run Hash Command**
img_path=""
if st.session_state.verified and st.session_state.pan_verified:
    img_path = "../Img.png"

    # Save the verified PAN card image
    with open(img_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Run terminal command and capture output
    pan_number = st.session_state.pan_number
    command = f'cd .. && python3 python_hash2.py Img.png "{pan_number}"'  # Fix path issues

    try:
        result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = result.communicate()

        # Decode the output and store in session
        st.session_state.output = output.decode("utf-8").strip()

        st.success("✅ Image saved and hash computation executed successfully!")

    except Exception as e:
        st.error(f"❌ Error executing script: {e}")
contract_address=""
# 🌟 **Step 5: Display the Process Output**
if st.session_state.output:
    st.subheader("📜 Process Output")
    st.text(st.session_state.output)

    # Extract Contract Address if available
    match = re.search(r"🚀 Contract deployed at: (0x[a-fA-F0-9]+)", st.session_state.output)
    if match:
        contract_address = match.group(1)
        st.success(f"**✅ Smart Contract Address:** `{contract_address}`")


# 🌟 Step 6: Upload to IPFS using Pinata
st.subheader("🛰️ Upload Verified PAN to IPFS")



def upload_file_to_ipfs(pil_image: Image.Image, pan_number: str) -> str:
    """
    Uploads a PIL Image object to IPFS using Pinata.

    Args:
        pil_image (PIL.Image): Encrypted image object.
        pan_number (str): Used to name the file for Pinata.

    Returns:
        str: IPFS gateway URL to access the uploaded file.
    """
    url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
    headers = {
        "pinata_api_key": PINATA_API_KEY,
        "pinata_secret_api_key": PINATA_SECRET_API_KEY,
    }

    # Convert PIL Image to bytes
    img_byte_arr = io.BytesIO()
    pil_image.save(img_byte_arr, format="PNG")
    img_byte_arr.seek(0)

    files = {
        "file": (f"{pan_number}_verified.png", img_byte_arr)
    }

    response = requests.post(url, files=files, headers=headers)

    if response.status_code == 200:
        ipfs_hash = response.json()["IpfsHash"]
        return f"https://gateway.pinata.cloud/ipfs/{ipfs_hash}"
    else:
        raise Exception(f"Failed to upload: {response.text}")

    
def encrypt_uploaded_image(uploaded_file, contract_address: str) -> Image.Image:
    """
    Encrypts an uploaded image using a smart contract address via XOR encryption.

    Args:
        uploaded_file: Streamlit UploadedFile object (from st.file_uploader).
        contract_address (str): Ethereum smart contract address used for encryption.

    Returns:
        PIL.Image: Encrypted image object.
    """
    # Load and convert image to RGB
    image = Image.open(uploaded_file).convert("RGB")
    img_array = np.array(image)

    # Generate key stream from contract address
    hash_seed = hashlib.sha256(contract_address.encode('utf-8')).digest()
    key_stream = np.frombuffer(hash_seed * ((img_array.size // len(hash_seed)) + 1), dtype=np.uint8)
    key_stream = key_stream[:img_array.size].reshape(img_array.shape)

    # XOR the image pixels with the key stream
    encrypted_array = np.bitwise_xor(img_array, key_stream)

    # Return encrypted image
    encrypted_image = Image.fromarray(encrypted_array.astype(np.uint8))
    return encrypted_image

# Only trigger if image hash step completed
if st.session_state.output and st.button("📡 Upload to IPFS"):
    try:
        encrypted_img = encrypt_uploaded_image(uploaded_file, contract_address)
        ipfs_url = upload_file_to_ipfs(encrypted_img, st.session_state.pan_number)
        st.success("✅ Uploaded to IPFS successfully!")
        st.markdown(f"📎 [View on IPFS]({ipfs_url})")
    except Exception as e:
        st.error(f"❌ IPFS upload failed: {e}")
