from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
# from webdriver_manager.core.os_manager import ChromeType
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import chromedriver_autoinstaller

chromedriver_autoinstaller.install()  # Check if the current version of chromedriver exists
                                      # and if it doesn't exist, download it automatically,
                                      # then add chromedriver to path

# executable_path = ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
# chrome_service = Service(executable_path=executable_path)

chrome_options = Options()
options = [
    "--headless",
    "--disable-gpu",
    "--window-size=1920,1200",
    "--ignore-certificate-errors",
    "--disable-extensions",
    "--no-sandbox",
    "--disable-dev-shm-usage"
]
for option in options:
    chrome_options.add_argument(option)

driver = webdriver.Chrome(options=chrome_options)

# Load the Facebook page
driver.get("https://www.facebook.com/JSPWellnessBoneAlignme/live_videos")

# Wait for the page to load and the modal to appear
wait = WebDriverWait(driver, 10)

try:
    # Wait for the modal to appear and close it
    close_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[aria-label='Close']")))
    close_button.click()
except:
    print("No modal found or already closed.")


iteration = 0
# Scroll to the bottom of the page
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    # Scroll down to the bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait for new page segment to load
    time.sleep(2)  # You can adjust the sleep time as needed

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height or iteration == 10:
        break
    last_height = new_height
    iteration += 1



# Save the page as HTML
html_content = driver.page_source
file_name = "facebook_page.html"

with open(file_name, "w", encoding="utf-8") as file:
    file.write(html_content)

# Close the WebDriver
driver.quit()

print(f"Page saved as '{file_name}'.")