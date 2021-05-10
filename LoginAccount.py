from MyConstants import Facebook
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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


def getDataFace(driver):
    print(driver.title)
