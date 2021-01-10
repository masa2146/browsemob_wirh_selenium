from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Firefox()
driver.get("http://www.sreality.cz/hledani/prodej/domy?region=jemnice")
driver.maximize_window()

wait = WebDriverWait(driver, 10)
wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "property")))

links = [link.get_attribute("href") for link in driver.find_elements_by_css_selector("div.property div.info a")]
print(links)

driver.close()