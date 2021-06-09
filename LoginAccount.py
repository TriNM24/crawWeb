from warnings import catch_warnings
from MyConstants import Facebook
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pickle
import os
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from html import unescape


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


def getDataFace(driver):
    print('get data' + driver.title)
    CONT = Facebook()  
    driver.get("https://www.facebook.com/" + CONT.nameSearch)   
    try:
        try:
            #try to get fanpage group name
            elementFanpageName = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, CONT.fanpageGroupName)))
            name = elementFanpageName.get_attribute('innerHTML')
            print(name)
            elementFanpageMember = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, CONT.fanpageGroupMember)))
            member = elementFanpageMember.get_attribute('innerHTML')
            print(member)
        except Exception as ex:
            try:
                # try to get fanpage
                elementFanpage = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, CONT.fanpageImage)))
                image = elementFanpage.get_attribute('innerHTML')        
                start = image.find("https://")
                end = image.find("></image>")
                image = image[start:end-1]
                image = unescape(image)
                print(image)
                elementFanpageName = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, CONT.fanpageName)))
                name = elementFanpageName.get_attribute('innerHTML')
                print(name)

            except Exception as ex:
                # get image and name of user
                element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, CONT.userImage)))
                image = element.get_attribute('innerHTML')        
                start = image.find("https://")
                end = image.find("></image>")
                image = image[start:end-1]
                image = unescape(image)
                name = element.get_attribute('aria-label') 
                print(name)
                print(image)
                try:
                    elementFollower = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, CONT.userFollower)))
                    follower = elementFollower.get_attribute('innerHTML')
                    print(follower)
                except Exception as ex:
                    print("Do not have follwer")        
    except Exception as ex:
        print(ex)
