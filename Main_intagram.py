import sys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import pickle
import Constant_intagram as constant
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
# import loginaccount as login
# set endcoding
sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')
driver = webdriver.Firefox()
# init domain
# driver.get("https://www.instagram.com/")
try:
    cookies = pickle.load(open("cookies_integram.pkl", "rb"))
    driver.delete_all_cookies()
    for cookie in cookies:
        driver.add_cookie(cookie)
    print('Load cookies successfully')
except Exception as e:
    print("Can not load cookies " + str(e))
# reload to login via cookies
driver.get("https://www.instagram.com/accounts/login/")

xpathCheck = "//div[text()='Log In']"
try:
    tableInfor = WebDriverWait(driver, constant.defautWait).until(
        EC.presence_of_element_located((By.XPATH, xpathCheck)))
    print('Login')
    mail = driver.find_element_by_xpath(constant.xpathMail)
    mail.clear()
    mail.send_keys('aaaaaaa')
    passElement = driver.find_element_by_xpath(constant.xpathPass)
    passElement.clear()
    passElement.send_keys('bbbbbbb')

    buttonLogin = driver.find_element_by_xpath(constant.xpathButtonLogin)
    print('Submit button ' + buttonLogin.text)
    buttonLogin.click()

except NoSuchElementException as noelementex:
    print('Allready login')
except Exception as ex:
    print("Unknow error:{}".format(ex))
input('Press to exit')
driver.close()
quit()
