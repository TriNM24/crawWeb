import sys
from seleniumwire import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import pickle
import Constant_intagram as constant
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pickle
import os
# import loginaccount as login
# set endcoding
sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')


def interceptorRequest(request):
    a = 0
    # print("request: {}".format(request.path))
    # request.abort()


print("_________start_________")
profile = webdriver.FirefoxProfile()
profile.set_preference('intl.accept_languages', 'en-US, en')
driver = webdriver.Firefox(firefox_profile=profile)
driver.request_interceptor = interceptorRequest
# init domain
driver.get("https://www.instagram.com/")
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

try:
    buttonNotNowNotification = WebDriverWait(driver, constant.defautWait).until(
        EC.presence_of_element_located((By.XPATH, constant.notNowButtonNotification)))
    print("click butotn not now allow notification")
    action = ActionChains(driver)
    action.move_to_element(buttonNotNowNotification).click(
        buttonNotNowNotification).perform()
except Exception as ex:
    print("Try to click button not allow notification: {}".format(ex))

xpathCheck = "//div[text()='Log In']"
try:
    tableInfor = WebDriverWait(driver, constant.defautWait).until(
        EC.presence_of_element_located((By.XPATH, xpathCheck)))
    print('Login')
    mail = driver.find_element_by_xpath(constant.xpathMail)
    mail.clear()
    mail.send_keys(constant.userName)
    passElement = driver.find_element_by_xpath(constant.xpathPass)
    passElement.clear()
    passElement.send_keys(constant.passWord)

    buttonLogin = driver.find_element_by_xpath(constant.xpathButtonLogin)
    print('Submit button ' + buttonLogin.text)
    buttonLogin.click()
    try:
        action = ActionChains(driver)
        buttonNotNow = WebDriverWait(driver, constant.defautWait).until(
            EC.presence_of_element_located((By.XPATH, constant.notNowButtonSaveInfo)))
        print("click butotn not now in save information")
        time.sleep(2)
        action.move_to_element(buttonNotNow).click(buttonNotNow).perform()
        time.sleep(5)
        buttonNotNow2 = WebDriverWait(driver, constant.defautWait).until(
            EC.presence_of_element_located((By.XPATH, constant.notNowButtonNotification)))
        print("click butotn not now allow notification")
        action2 = ActionChains(driver)
        action2.move_to_element(buttonNotNow2).click(buttonNotNow2).perform()
        # save cookies
        if os.path.exists(constant.cookies_file):
            os.remove(constant.cookies_file)
            print('remove file {}'.format(constant.cookies_file))
        pickle.dump(driver.get_cookies(), open(
            constant.cookies_file, "wb"))
        print("Login and save cookies success")
    except Exception as ex:
        print("Button not now:{}".format(ex))

except NoSuchElementException as noelementex:
    print('Allready login')
except Exception as ex:
    print("Unknow error:{}".format(ex))

input('Press to exit')
driver.close()
quit()
