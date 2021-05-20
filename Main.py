import sys
from selenium import webdriver
import LoginAccount
import pickle
# import loginaccount as login
# set endcoding
sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')
driver = webdriver.Firefox()
# init domain
driver.get("https://www.facebook.com/")
try:
    cookies = pickle.load(open("cookies.pkl", "rb"))
    driver.delete_all_cookies()
    for cookie in cookies:
        driver.add_cookie(cookie)
    print('Load cookies successfully')
except Exception as e:
    print("Can not load cookies " + str(e))
# reload to login via cookies
driver.get("https://www.facebook.com/")

if 'đăng nhập' in driver.title.lower() or 'log in' in driver.title.lower():
    print('Login')
    LoginAccount.loginFace(driver)
else:
    print('Allready login')
LoginAccount.getDataFace(driver)
