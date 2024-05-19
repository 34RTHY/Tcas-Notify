import os
import time
import difflib
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from datetime import datetime
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

# Path to the saved page content
CONTENT_FILE = 'Generatedcontent/page_content.html'

# Configure WebDriver options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run headless for non-GUI mode
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Initialize WebDriver
service = Service(CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service, options=chrome_options)

def login():
    driver.get(LOGIN_URL)
    print('Logging in')
    time.sleep(5)

    # Enter ID and click the first login button
    user_id_field = driver.find_element(By.XPATH, '//input[@type="text" and @required]')
    login_button_1 = driver.find_element(By.XPATH, '//a[@class="btn-main cursor-pointer disabled"]')

    user_id_field.send_keys(USER_ID)

    # Scroll to the element and click using JavaScript to avoid interception issues
    driver.execute_script("arguments[0].scrollIntoView(true);", login_button_1)
    driver.execute_script("arguments[0].click();", login_button_1)
    print('Inputting password')
    time.sleep(5)  # Wait for the password field to appear

    # Enter password and click the second login button
    password_field = driver.find_element(By.XPATH, '//input[@type="password" and @placeholder="กรอกรหัสผ่าน"]')
    login_button_2 = driver.find_element(By.XPATH, '//a[@class="btn-main cursor-pointer"]')

    password_field.send_keys(PASSWORD)

    # Scroll to the element and click using JavaScript to avoid interception issues
    driver.execute_script("arguments[0].scrollIntoView(true);", login_button_2)
    driver.execute_script("arguments[0].click();", login_button_2)
    print('Waiting for the profile page to load')
    time.sleep(5)  # Wait for the profile page to load

def get_page_content(url):
    driver.get(url)
    print('Waiting for profile page to load')
    time.sleep(5)  # Wait for the page to load
    return driver.page_source

def read_saved_content(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    return ""

def clean_content(content):
    # Use BeautifulSoup to parse HTML and remove unwanted tags and attributes
    soup = BeautifulSoup(content, 'html.parser')

    # Remove script and meta tags
    for tag in soup.find_all(['script', 'meta']):
        tag.decompose()

    # Replace dynamic parts of the URLs in img src attributes
    for img in soup.find_all('img'):
        if 'src' in img.attrs:
            img['src'] = 'DYNAMIC_URL'

    # Convert the cleaned HTML back to string
    cleaned_html = soup.prettify()
    
    return cleaned_html

def print_differences(old_content, new_content):
    diff = difflib.unified_diff(
        old_content.splitlines(), 
        new_content.splitlines(), 
        fromfile='previous_content', 
        tofile='current_content', 
        lineterm=''
    )
    for line in diff:
        print(line)

def monitor_changes():
    login()  # Perform login
    previous_content = read_saved_content(CONTENT_FILE)
    current_content = get_page_content(TARGET_URL)

    # Clean the content to remove dynamic parts
    cleaned_previous_content = clean_content(previous_content)
    cleaned_current_content = clean_content(current_content)

    if cleaned_current_content != cleaned_previous_content:
        print(f"Page content has changed at {datetime.now()}.")
        print_differences(cleaned_previous_content, cleaned_current_content)
    else:
        print(f"No change detected at {datetime.now()}.")

if __name__ == "__main__":
    try:
        while True:
            monitor_changes()
            time.sleep(60)  # Wait for 60 seconds before checking again
    finally:
        driver.quit()