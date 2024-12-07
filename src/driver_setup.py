# # driver_setup.py

# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from config import CHROMEDRIVER_PATH, HEADLESS_MODE

# def setup_driver():
#     """Initialize and configure the WebDriver."""
#     service = Service(CHROMEDRIVER_PATH)
#     options = webdriver.ChromeOptions()
#     # if HEADLESS_MODE:
#     #     options.add_argument("--headless")
#     # options.add_argument("--no-sandbox")
#     options.add_argument("--disable-dev-shm-usage")
#     driver = webdriver.Chrome(service=service, options=options)
#     return driver


from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from config import GECKODRIVER_PATH, HEADLESS_MODE
from selenium.webdriver.firefox.options import Options

def setup_driver():
    """Initialize and configure the WebDriver for Firefox."""
    service = Service(GECKODRIVER_PATH)
    options = Options()
    options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"  # Update this path if necessary

    driver = webdriver.Firefox(service=service, options=options)
    return driver
