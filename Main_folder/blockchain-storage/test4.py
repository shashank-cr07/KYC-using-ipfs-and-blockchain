#test4.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Configuration - UPDATE THESE VALUES
CONFIG={
    "pan_number": "BNZPM2501F",
    "dob": "1986-07-16",
    "full_name": "Test Name",
    "chrome_profile_path": "/home/shashank/.config/google-chrome",  #Change this 
    "profile_name": "Default",  #Mostly is deafault
    "url": "https://apicentral.idfy.com/verify_with_source/ind_pan",
    "login_url": "https://apicentral.idfy.com/sessions/new",
    "email": "",            #Set your email and password in the website above this line
    "password": "",
    "timeout": 60
}


def setup_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f"--user-data-dir={CONFIG['chrome_profile_path']}")
    chrome_options.add_argument(f"--profile-directory={CONFIG['profile_name']}")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)


def login():
    driver = setup_driver()
    try:
        driver.get(CONFIG['login_url'])
        WebDriverWait(driver, CONFIG['timeout']).until(
            EC.presence_of_element_located((By.ID, "session_company_email"))
        )
        driver.find_element(By.ID, "session_company_email").send_keys(CONFIG['email'])
        driver.find_element(By.ID, "userLPassword").send_keys(CONFIG['password'])
        driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary").click()
        WebDriverWait(driver, CONFIG['timeout']).until(
            EC.url_contains("/ftue")
        )
        print("✅ Login successful!")
        time.sleep(3)
    except Exception as e:
        print(f"❌ Login failed: {str(e)}")
        raise
    finally:
        driver.quit()


def verify_pan(pan_number, dob):
    print("🚨 Ensure Chrome is completely closed before running this script!")
    login()
    driver = setup_driver()
    try:
        driver.delete_all_cookies()

        driver.get(CONFIG['url'])
        WebDriverWait(driver, CONFIG['timeout']).until(
            EC.presence_of_element_located((By.ID, "api_params_id_number"))
        )
        time.sleep(2)  # Ensure page is fully loaded

        driver.find_element(By.ID, "api_params_id_number").send_keys(pan_number)
        dob_field = driver.find_element(By.ID, "api_params_dob")
        driver.execute_script(f"arguments[0].value = '{dob}'", dob_field)
        driver.find_element(By.ID, "api_params_full_name").send_keys(CONFIG['full_name'])
        submit_button = WebDriverWait(driver, CONFIG['timeout']).until(
            EC.element_to_be_clickable((By.ID, "submit-button-string"))
        )

        while "disabled" in submit_button.get_attribute("class"):
            print("⏳ Waiting for the button to become enabled...")
            time.sleep(1)
            submit_button = driver.find_element(By.ID, "submit-button-string")

        driver.execute_script("arguments[0].click();", submit_button)
        print("✅ Form submitted successfully!")

        time.sleep(5)  # Wait after submission to allow processing

        WebDriverWait(driver, CONFIG['timeout']).until(
            EC.invisibility_of_element_located((By.ID, "loading-gif"))
        )

        status = driver.find_element(By.ID, "status-code-content").text.strip()

        # Get JSON Response
        json_result = "Not available"
        try:
            json_tab = WebDriverWait(driver, CONFIG['timeout']).until(
                EC.element_to_be_clickable((By.ID, "json-button"))
            )
            driver.execute_script("arguments[0].click();", json_tab)
            time.sleep(2)  # Allow time for the JSON view to load
            json_result = driver.find_element(By.ID, "json-response-area").text.strip()
        except Exception:
            pass

        return {"status": status, "json_result": json_result}

    except Exception as e:
        return {"error": str(e)}
    finally:
        driver.quit()


def main():
    print("🚨 Ensure Chrome is completely closed before running this script!")
    login()
    print("🔄 Reopening Chrome for verification...")
    verify_pan(CONFIG["pan_number"], CONFIG["dob"])


if __name__ == "__main__":
    main()
