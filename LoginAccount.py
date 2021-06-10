from warnings import catch_warnings
from MyConstants import Facebook
from MyConstants import Intagram
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pickle
import os
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from html import unescape
import Constant_intagram as constant
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains


def loginIntagram(driver):
    constant = Intagram()
    print('Login')
    xpathCheck = "//div[text()='Log In']"
    try:
        tableInfor = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpathCheck)))
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
            buttonNotNow = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, constant.notNowButtonSaveInfo)))
            print("click butotn not now in save information")
            time.sleep(2)
            action.move_to_element(buttonNotNow).click(buttonNotNow).perform()
            time.sleep(5)
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
        print('Can not find button login')


def loginFace(driver):
    print(driver.title)
    CONT = Facebook()
    mail = driver.find_element_by_xpath(CONT.xpathEmail)
    mail.clear()
    mail.send_keys(CONT.facebookUser)

    passInput = driver.find_element_by_xpath(CONT.xpathPass)
    passInput.clear()
    passInput.send_keys(CONT.facebookPass)

    buttonSubmit = driver.find_element_by_xpath(CONT.xpathSubmit)
    print('Submit button ' + buttonSubmit.text)
    buttonSubmit.click()
    WebDriverWait(driver, 10).until(EC.title_is('Facebook'))
    if os.path.exists("cookies.pkl"):
        os.remove("cookies.pkl")
        print('remove file cookies.pkl')
    pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))


def getDataFace(driver, nameSearch):
    print('get data' + driver.title)
    CONT = Facebook()
    driver.get("https://www.facebook.com/" + nameSearch)
    try:
        try:
            # try to get fanpage group name
            elementFanpageName = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, CONT.fanpageGroupName)))
            name = elementFanpageName.get_attribute('innerHTML')
            print(name)
            elementFanpageMember = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, CONT.fanpageGroupMember)))
            member = elementFanpageMember.get_attribute('innerHTML')
            print(member)
        except Exception as ex:
            try:
                # try to get fanpage
                elementFanpage = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, CONT.fanpageImage)))
                image = elementFanpage.get_attribute('innerHTML')
                start = image.find("https://")
                end = image.find("></image>")
                image = image[start:end-1]
                image = unescape(image)
                print(image)
                elementFanpageName = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, CONT.fanpageName)))
                name = elementFanpageName.get_attribute('innerHTML')
                print(name)

            except Exception as ex:
                # get image and name of user
                element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, CONT.userImage)))
                image = element.get_attribute('innerHTML')
                start = image.find("https://")
                end = image.find("></image>")
                image = image[start:end-1]
                image = unescape(image)
                name = element.get_attribute('aria-label')
                print(name)
                print(image)
                try:
                    elementFollower = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, CONT.userFollower)))
                    follower = elementFollower.get_attribute('innerHTML')
                    print(follower)
                except Exception as ex:
                    print("Do not have follwer")
    except Exception as ex:
        print(ex)
