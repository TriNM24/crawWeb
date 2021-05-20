from warnings import catch_warnings
from MyConstants import Facebook
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pickle
import os
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By


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
    # searchBox = driver.find_element_by_xpath(CONT.searchBox)
    # searchBox.clear()
    # searchBox.send_keys(CONT.nameSearch)
    # searchBox.submit()
    # time.sleep(2)
    # searchBox.send_keys(Keys.ENTER)

    # get all photo
    driver.get("https://www.facebook.com/" + CONT.nameSearch + '/photos')
    try:
        xpathImage = '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[1]/div/div/div/div/div[3]/div'
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpathImage)))
        result = driver.find_element_by_xpath(xpathImage)
        test = result.get_attribute('innerHTML')
        # print(test)
        imgs = result.find_elements_by_xpath("//img[contains(@src, '')]")
        for img in imgs:
            print(img.get_attribute('src'))
        # pageSource = driver.page_source
        # bsObj = BeautifulSoup(pageSource, 'html.parser')
        # prettyHTML = bsObj.prettify()
        # print(prettyHTML)

        # links = driver.find_elements_by_xpath('//cite')
        # for link in links:
        #     print(link.text)
    except Exception as e:
        print(e)
