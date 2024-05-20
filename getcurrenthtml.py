import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json

CHROME_DRIVER_PATH = r'./chromedriver-win64/chromedriver.exe'

# URLs
LOGIN_URL = 'https://student.mytcas.com/'
TARGET_URL = 'https://student.mytcas.com/profile'

# Login credentials
with open('./Credentials/credentials.json', 'r') as file:
    config = json.load(file)
    USER_ID = config['user_id']
    PASSWORD = config['password']

# Configure WebDriver options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Initialize WebDriver
service = Service(CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service, options=chrome_options)

def login():
    print('logging in')
    driver.get(LOGIN_URL)
    time.sleep(5)

    #Enter ID and click the first login button
    user_id_field = driver.find_element(By.XPATH, '//input[@type="text" and @required]')
    login_button_1 = driver.find_element(By.XPATH, '//a[@class="btn-main cursor-pointer disabled"]')

    user_id_field.send_keys(USER_ID)

    # Scroll to the element and click using JavaScript to avoid interception issues
    driver.execute_script("arguments[0].scrollIntoView(true);", login_button_1)
    driver.execute_script("arguments[0].click();", login_button_1)
    time.sleep(5)

    #Enter password and click the second login button
    password_field = driver.find_element(By.XPATH, '//input[@type="password" and @placeholder="กรอกรหัสผ่าน"]')
    login_button_2 = driver.find_element(By.XPATH, '//a[@class="btn-main cursor-pointer"]')
    password_field.send_keys(PASSWORD)

    # Scroll to the element and click using JavaScript to avoid interception issues
    driver.execute_script("arguments[0].scrollIntoView(true);", login_button_2)
    driver.execute_script("arguments[0].click();", login_button_2)

    time.sleep(5)

def get_page_content(url):
    driver.get(url)
    time.sleep(5)
    return driver.page_source

def monitor_changes():
    login()
    current_content = get_page_content(TARGET_URL)
    with open("./Generatedcontent/page_content.html", "w", encoding="utf-8") as file:
        file.write(current_content)

if __name__ == "__main__":
    try:
        monitor_changes()
    finally:
        driver.quit()
