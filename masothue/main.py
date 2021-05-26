import os
import ulty.ulties as ulties
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import sys
sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

# scroll to element


def scroll_shim(passed_in_driver, object):
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
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, xpathData)))
    scroll_shim(driver, element)
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
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, xpathPageNumber)))
    scroll_shim(driver, element)
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
    elementCurrentPage = WebDriverWait(passedDriver, 10).until(
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
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, xpathDismiss)))
    element.click()

provinesElement = driver.find_element_by_xpath(xpathProvines)
provines = provinesElement.find_elements_by_xpath("./li/a")
# for provine in provines:
#     print(provine.get_attribute('innerHTML'))
# go to and click provine
action = ActionChains(driver)
action.move_to_element(provines[28])
provines[28].click()
# start get data of provine
getDataProvine(driver, "Ho_Chi_Minh")

quit()
