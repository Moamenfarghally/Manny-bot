from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

print("Starting Chrome...")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

print("Chrome started!")

driver.get("https://www.google.com")
print("Page title:", driver.title)

driver.quit()
print("DONE.")
