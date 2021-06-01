import random
import os
import ulty.ulties as ulties
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import sys
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import NoSuchElementException

sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

defautWait = 30

def scroll_shim(passed_in_driver, object):  # scroll to element
    x = object.location['x']
    y = object.location['y']
    scroll_by_coord = 'window.scrollTo(%s,%s);' % (x, y)
    scroll_nav_out_of_way = 'window.scrollBy(0, -120);'
    passed_in_driver.execute_script(scroll_by_coord)
    passed_in_driver.execute_script(scroll_nav_out_of_way)


def getdataDetail(passedDriver, provineName):
    print(passedDriver.title)
    tableInforXpath = "//table[@class='table-taxinfo']"
    try:
        tableInfor = WebDriverWait(passedDriver, defautWait).until(
            EC.presence_of_element_located((By.XPATH, tableInforXpath)))
        # tableInfor = passedDriver.find_element_by_xpath(tableInforXpath)
        companyNameXpath = "./thead//span"
        companyName = tableInfor.find_element_by_xpath(
            companyNameXpath).get_attribute('innerHTML')
        print(companyName)

        informationsXpath = "./tbody/tr"
        informations = tableInfor.find_elements_by_xpath(informationsXpath)
        dataXpath1 = ".//span"
        dataXpath2 = ".//a"
        # get all tax info
        for information in informations:
            try:
                info = information.find_element_by_xpath(dataXpath1)
            except NoSuchElementException as ex:
                try:
                    info = information.find_element_by_xpath(dataXpath2)
                except Exception as ex:
                    info = None
            if(info != None):
                data = ulties.cleanhtml(info.get_attribute('innerHTML'))
                ulties.writeData(data, provineName)

        # get all business
        tableBusinessXpath = "//table[@class='table']"
        tableBusiness = passedDriver.find_element_by_xpath(tableBusinessXpath)
        businessXpath = "./tbody/tr/td[2]//a"
        businesses = tableBusiness.find_elements_by_xpath(businessXpath)
        ulties.writeData('___Business___', provineName)
        for business in businesses:
            data = ulties.cleanhtml(business.get_attribute('innerHTML'))
            ulties.writeData(data, provineName)
    except Exception as ex:
        print("Error when get detail: {}".format(ex))



def getDataOnePage(passedDriver, provineName):
    # get data
    print(passedDriver.title)
    xpathData = "//div[@class='tax-listing']"
    element = WebDriverWait(passedDriver, defautWait).until(
        EC.presence_of_element_located((By.XPATH, xpathData)))
    scroll_shim(passedDriver, element)
    companies = element.find_elements_by_xpath("./div")
    for company in companies:
        titleDetail = company.find_element_by_xpath("./h3/a")
        scroll_shim(passedDriver, titleDetail)
        # wait before open new tab
        wait = random.randint(10, 30)
        print("Wait {} second to open detail".format(wait))
        time.sleep(wait)
        # go to detail
        action = ActionChains(passedDriver)
        action.move_to_element(titleDetail).key_down(Keys.CONTROL).click(
            titleDetail).key_up(Keys.CONTROL).perform()
        # switch tab to last
        passedDriver.switch_to.window(passedDriver.window_handles[-1])
        getdataDetail(passedDriver, provineName)
        # wait before close detail tab
        wait = random.randint(10, 30)
        print("Wait {} second to close detail".format(wait))
        time.sleep(wait)
        # switch tab to last
        passedDriver.close()
        passedDriver.switch_to.window(passedDriver.window_handles[-1])       
        # testt
        # break 


def getDataProvine(passedDriver, provineName):
    getDataOnePage(passedDriver, provineName)
    # move to next page
    xpathPageNumber = "//ul[@class='page-numbers']"
    xpathCurrentPageNumber = "//ul[@class='page-numbers']/li/span"
    element = WebDriverWait(passedDriver, defautWait).until(
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
            wait = random.randint(10, 30)
            print("Wait {} second to go next page".format(wait))
            time.sleep(wait)
            nexPage.click()
            break
    elementCurrentPage = WebDriverWait(passedDriver, defautWait).until(
        EC.presence_of_element_located((By.XPATH, xpathCurrentPageNumber)))
    currentPageNumber = elementCurrentPage.get_attribute('innerHTML')
    if(currentPageNumber == nexpageNum):
        getDataProvine(passedDriver, provineName)
    else:
        print("Finhish for this provine")


print('start')
# seed random number generator
random.seed(time.perf_counter())

driver = ulties.build_driver()
driver.get('https://masothue.com/')
xpathProvines = "//ul[@class='row']"

element = WebDriverWait(driver, defautWait).until(
    EC.presence_of_element_located((By.XPATH, xpathProvines)))

provinesElement = driver.find_element_by_xpath(xpathProvines)
provines = provinesElement.find_elements_by_xpath("./li/a")

count = 0
for provine in provines:
    if(count < 100):
        count = count + 1
        provineTitle = provine.get_attribute('innerHTML')
        provineTitle = provineTitle[provineTitle.find("/span>")+6:].strip()
        ulties.writeData("_______{}_______".format(provineTitle), "DataCraw")
        # open link with new tab
        action = ActionChains(driver)
        scroll_shim(driver, provine)
        # wait before open new tab
        wait = random.randint(10, 30)
        print("Wait {} second to open provine".format(wait))
        time.sleep(wait)
        action.move_to_element(provine).key_down(Keys.CONTROL).click(
            provine).key_up(Keys.CONTROL).perform()
        # switch tab to last
        driver.switch_to.window(driver.window_handles[-1])
        # start get data of provine
        getDataProvine(driver, "DataCraw")
        # close all tabs without first tab
        wait = random.randint(10, 30)
        print("Wait {} second to close provine tab".format(wait))
        time.sleep(wait)
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
