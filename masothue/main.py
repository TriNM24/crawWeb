import os
import ulty.ulties as ulties
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

print('start')
driver = ulties.build_driver()
print(driver.title)
driver.get('https://masothue.com/')
print(driver.title)
xpathProvines = "//ul[@class='row']"
element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, xpathProvines)))
provines = element.find_elements_by_xpath("//li/a")
for provine in provines:
    print(provine.get_attribute('innerHTML'))
# test = element.get_attribute('innerHTML')
# print(test)
quit()
