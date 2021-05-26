import os
import ulty.ulties as ulties
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import sys
from selenium.webdriver.common.keys import Keys
import time

sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')


def scroll_shim(passed_in_driver, object):  # scroll to element
    x = object.location['x']
    y = object.location['y']
    scroll_by_coord = 'window.scrollTo(%s,%s);' % (x, y)
    scroll_nav_out_of_way = 'window.scrollBy(0, -120);'
    passed_in_driver.execute_script(scroll_by_coord)
    passed_in_driver.execute_script(scroll_nav_out_of_way)


def getDataOnePage(passedDriver, provineName):
    # get data
    print(passedDriver.title)
    xpathData = "//div[@class='tax-listing']"
    element = WebDriverWait(passedDriver, 20).until(
        EC.presence_of_element_located((By.XPATH, xpathData)))
    scroll_shim(passedDriver, element)
    companies = element.find_elements_by_xpath("./div")
    # test company 1
    # print(companies[0].get_attribute('innerHTML'))
    for company in companies:
        title = company.find_element_by_xpath(
            "./h3/a").get_attribute('innerHTML')
        taxNumber = company.find_element_by_xpath(
            "./div/a").get_attribute('innerHTML')
        owner = company.find_element_by_xpath(
            "./div/em/a").get_attribute('innerHTML')
        address = company.find_element_by_xpath(
            "./address").get_attribute('innerHTML')
        addressResult = address[address.find("/i>")+3:].strip()
        print(title)
        print(taxNumber)
        print(owner)
        print(address)
        ulties.writeData("{}\n{}\n{}\n{}".format(
            title, taxNumber, owner, addressResult), provineName)


def getDataProvine(passedDriver, provineName):
    getDataOnePage(passedDriver, provineName)
    # move to next page
    xpathPageNumber = "//ul[@class='page-numbers']"
    xpathCurrentPageNumber = "//ul[@class='page-numbers']/li/span"
    element = WebDriverWait(passedDriver, 20).until(
        EC.presence_of_element_located((By.XPATH, xpathPageNumber)))
    scroll_shim(passedDriver, element)
    pages = element.find_elements_by_xpath("./li")
    isHaveCurrent = False
    nexpageNum = 0
    for page in pages:
        if(isHaveCurrent == False):
            try:
                page.find_element_by_xpath("./span")
                isHaveCurrent = True
            except Exception as ex:
                sHaveCurrent = False
        else:
            # move to next page
            nexPage = page.find_element_by_xpath("./a")
            nexpageNum = nexPage.get_attribute('innerHTML')
            print("____________next page____________:{}".format(nexpageNum))
            nexPage.click()
            break
    elementCurrentPage = WebDriverWait(passedDriver, 20).until(
        EC.presence_of_element_located((By.XPATH, xpathCurrentPageNumber)))
    currentPageNumber = elementCurrentPage.get_attribute('innerHTML')
    if(currentPageNumber == nexpageNum):
        getDataProvine(passedDriver, provineName)
    else:
        print("Finhish for this provine")


print('start')
driver = ulties.build_driver()
driver.get('https://masothue.com/')
xpathProvines = "//ul[@class='row']"
xpathDismiss = "//div[@id = 'dismiss-button']"
try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, xpathProvines)))
except Exception as ex:
    print("Have advertisement")
    # option 1
    driver.find_element_by_xpath("//body").click()
    # option 2
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, xpathDismiss)))
    element.click()
# click to prenvet popup advertisement
driver.find_element_by_xpath("//body").click()

provinesElement = driver.find_element_by_xpath(xpathProvines)
provines = provinesElement.find_elements_by_xpath("./li/a")

# action = ActionChains(driver)
# scroll_shim(driver, provines[0])
# action.move_to_element(provines[0]).key_down(Keys.CONTROL).click(
#     provines[0]).key_up(Keys.CONTROL).perform()

# quit()
count = 0
for provine in provines:
    if(count < 200):
        count = count + 1
        provineTitle = provine.get_attribute('innerHTML')
        provineTitle = provineTitle[provineTitle.find("/span>")+6:].strip()
        ulties.writeData("_______{}_______".format(provineTitle), "DataCraw")
        # open link with new tab
        action = ActionChains(driver)
        scroll_shim(driver, provine)
        action.move_to_element(provine).key_down(Keys.CONTROL).click(
            provine).key_up(Keys.CONTROL).perform()
        # provines[28].click()
        # switch tab to last
        driver.switch_to.window(driver.window_handles[-1])
        # start get data of provine
        # print(driver.title)
        getDataProvine(driver, "DataCraw")
        # close all tabs without first tab
        firstTime = True
        for handle in driver.window_handles:
            driver.switch_to.window(handle)
            if(not firstTime):
                driver.close()
            firstTime = False
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(5)
    else:
        break
quit()
