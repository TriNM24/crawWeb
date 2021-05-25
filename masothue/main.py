from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
import os
import ulty.ulties as ulties

print('start')
driver = ulties.build_driver()
print(driver.title)
driver.get('https://masothue.com/')
print(driver.title)
