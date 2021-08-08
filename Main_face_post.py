import sys
from time import time
from selenium import webdriver
import LoginAccount
import pickle
from MyConstants import Facebook
from fake_useragent import UserAgent
import FirefoxUlties

# set endcoding
sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

profile = webdriver.FirefoxProfile()
profile.set_preference('intl.accept_languages', 'en-US, en')
driver = webdriver.Firefox(firefox_profile=profile)
input("Press to get data after brower is ready")
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

CONT = Facebook()
LoginAccount.getFacePost(driver, CONT.nameSearch)

input('Press to exit')
driver.close()
quit()
