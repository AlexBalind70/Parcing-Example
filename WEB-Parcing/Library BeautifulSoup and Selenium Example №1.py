from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# create a ChromeOptions object to set options for the Chrome browser
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")  # maximize the window on start-up

# create a ChromeDriverManager instance to download and manage the driver executable
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

# navigate to a website
driver.get("https://www.nbcomputers.ru/")

# find the search box element and type a query
search_box = driver.find_element(By.XPATH, "//input[@type='search']")
search_box.send_keys("lenovo\n\n")

wait = WebDriverWait(driver, 10)
time.sleep(4)

load_more_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.digi-ac-find__button')))
load_more_button.click()

driver.quit()
