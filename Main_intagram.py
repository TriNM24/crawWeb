from MyConstants import Intagram
import sys
from seleniumwire import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import pickle
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pickle
import os
import FirefoxUlties
import LoginAccount
# import loginaccount as login
# set endcoding
sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')


def interceptorRequest(request):
    a = 0
    # print("request: {}".format(request.path))
    # request.abort()


print("_________start_________")
constant = Intagram()
driver = FirefoxUlties.createFirefox()
input("Press to get data after brower is ready")
driver.request_interceptor = interceptorRequest
# init domain
driver.get("https://www.instagram.com/accounts/login/")
try:
    cookies = pickle.load(open(constant.cookies_file, "rb"))
    driver.delete_all_cookies()
    for cookie in cookies:
        driver.add_cookie(cookie)
    print('Load cookies successfully')
except Exception as e:
    print("Can not load cookies " + str(e))
# reload to login via cookies
driver.get("https://www.instagram.com/accounts/login/")

if 'login' in driver.title.lower():
    LoginAccount.loginIntagram(driver)
else:
    print('Allready login')

# click button not allow notification if it popup
try:
    buttonNotNowNotification = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, constant.notNowButtonNotification)))
    print("click butotn not now allow notification")
    action = ActionChains(driver)
    action.move_to_element(buttonNotNowNotification).click(
        buttonNotNowNotification).perform()
except Exception as ex:
    print("Try to click button not allow notification: {}".format(ex))
LoginAccount.getInfoIntagram(driver, constant.nameSearch)
input('Press to exit')
driver.close()
quit()
