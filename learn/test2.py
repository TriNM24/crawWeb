from logging import exception
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
import os
import ulty.ulties as ulties
import time

print('start')
driver = ulties.build_driver()
print(driver.title)
driver.get('https://genk.vn/')
print(driver.title)
