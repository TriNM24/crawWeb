import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from LoginAccount import loginFace
# import loginaccount as login
# set endcoding
sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')
driver = webdriver.Firefox()
driver.get("https://www.facebook.com/")

if 'đăng nhập' in driver.title.lower() or 'log in' in driver.title.lower():
    print('contain')
    loginFace(driver)
print(driver.title)
