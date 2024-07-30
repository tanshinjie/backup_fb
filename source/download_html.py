from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from utils import resolve_path_to_file

# Initialize the WebDriver (e.g., Chrome)
service = Service(executable_path="/Users/shinjie/shinjie-workspace/backup-fb/chromedriver-mac-arm64/chromedriver")
options = Options()
options.add_argument("--headless=new")
driver = webdriver.Chrome(service=service, options=options)

# Load the Facebook page
url = "https://www.facebook.com/JSPWellnessBoneAlignme/live_videos"
driver.get(url)

# Wait for the page to load and the modal to appear
wait = WebDriverWait(driver, 10)

try:
    # Wait for the modal to appear and close it
    close_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[aria-label='Close']")))
    close_button.click()
except:
    print("No modal found or already closed.")

# Scroll to the bottom of the page
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    # Scroll down to the bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait for new page segment to load
    time.sleep(2)  # You can adjust the sleep time as needed

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Save the page as HTML
html_content = driver.page_source
file_name = "facebook_page.html"
output_file_path = resolve_path_to_file(f"output/{file_name}")
with open(output_file_path, "w", encoding="utf-8") as file:
    file.write(html_content)

# Close the WebDriver
driver.quit()

print(f"Page saved as '{file_name}'.")
