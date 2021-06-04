import random
import ulty.ulties as ulties
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import sys
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import NoSuchElementException
from seleniumwire import webdriver
import os
from selenium.webdriver.firefox.options import Options
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem


sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

defautWait = 30
refreshCount = 3


def getRandomTime():
    min = random.randint(10, 20)
    max = random.randint(30, 40)
    wait = random.randint(min, max)
    return wait


currentPath = ''


def interceptorRequest(request):
    global currentPath
    if(request.path == '/' or request.path == currentPath):
        ulties.writeLog('Allow request: {}'.format(request.path))
    else:
        ulties.writeLog('Abord request: {}'.format(request.path))
        request.abort()


def scroll_shim(passed_in_driver, object):  # scroll to element
    x = object.location['x']
    y = object.location['y']
    scroll_by_coord = 'window.scrollTo(%s,%s);' % (x, y)
    scroll_nav_out_of_way = 'window.scrollBy(0, -120);'
    passed_in_driver.execute_script(scroll_by_coord)
    passed_in_driver.execute_script(scroll_nav_out_of_way)


def getdataDetail(passedDriver, provineName):
    ulties.writeLog(passedDriver.title)
    tableInforXpath = "//table[@class='table-taxinfo']"
    try:
        tableInfor = WebDriverWait(passedDriver, defautWait).until(
            EC.presence_of_element_located((By.XPATH, tableInforXpath)))
        # tableInfor = passedDriver.find_element_by_xpath(tableInforXpath)
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
        try:
            tableBusinessXpath = "//table[@class='table']"
            tableBusiness = passedDriver.find_element_by_xpath(
                tableBusinessXpath)
            businessXpath = "./tbody/tr/td[2]//a"
            businesses = tableBusiness.find_elements_by_xpath(businessXpath)
            ulties.writeData('___Business___', provineName)
            for business in businesses:
                data = ulties.cleanhtml(business.get_attribute('innerHTML'))
                ulties.writeData(data, provineName)
        except Exception as ex:
            ulties.writeLog("Do not have business")
        ulties.writeData('--------------', provineName)
        return True
    except Exception as ex:
        ulties.writeLog("Error when get detail: {}".format(ex))
        return False


def openDeail(passedDriver, detailElement, provineName):
    global refreshCount
    action = ActionChains(passedDriver)
    action.move_to_element(detailElement).key_down(Keys.CONTROL).click(
        detailElement).key_up(Keys.CONTROL).perform()
    # switch tab to last
    passedDriver.switch_to.window(passedDriver.window_handles[-1])
    success = getdataDetail(passedDriver, provineName)
    if(success == False):
        if(refreshCount > 0):
            refreshCount = refreshCount - 1
            wait = getRandomTime()
            ulties.writeLog("Wait {} second to reopen page: count {}".format(
                wait, refreshCount))
            time.sleep(wait)
            passedDriver.close()
            passedDriver.switch_to.window(passedDriver.window_handles[-1])
            openDeail(passedDriver, detailElement, provineName)


def getDataOnePage(passedDriver, provineName):
    global refreshCount
    # get data
    ulties.writeLog(passedDriver.title)
    try:
        xpathData = "//div[@class='tax-listing']"
        element = WebDriverWait(passedDriver, defautWait).until(
            EC.presence_of_element_located((By.XPATH, xpathData)))
        scroll_shim(passedDriver, element)
        companies = element.find_elements_by_xpath("./div")
        for company in companies:
            titleDetail = company.find_element_by_xpath("./h3/a")
            scroll_shim(passedDriver, titleDetail)
            # wait before open new tab
            wait = getRandomTime()
            ulties.writeLog("Wait {} second to open detail".format(wait))
            time.sleep(wait)
            # go to detail
            refreshCount = 3
            openDeail(passedDriver, titleDetail, provineName)
            # wait before close detail tab
            wait = getRandomTime()
            ulties.writeLog("Wait {} second to close detail".format(wait))
            time.sleep(wait)
            # switch tab to last
            passedDriver.close()
            passedDriver.switch_to.window(passedDriver.window_handles[-1])
        return True
    except Exception as ex:
        ulties.writeLog('Exception get one page: {}'.format(ex))
        return False


def getDataProvine(passedDriver, provineName):
    result = getDataOnePage(passedDriver, provineName)
    if(result == True):
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
                wait = getRandomTime()
                ulties.writeLog("Wait {} second to go next page".format(wait))
                time.sleep(wait)
                nexPage = page.find_element_by_xpath("./a")
                nexpageNum = nexPage.get_attribute('innerHTML')
                ulties.writeLog(
                    "____________next page____________:{}".format(nexpageNum))
                nexPage.click()
                break
        elementCurrentPage = WebDriverWait(passedDriver, defautWait).until(
            EC.presence_of_element_located((By.XPATH, xpathCurrentPageNumber)))
        currentPageNumber = elementCurrentPage.get_attribute('innerHTML')
        ulties.writeLog("Current page:{} , Nextpage:{}".format(
            currentPageNumber, nexpageNum))
        if(currentPageNumber == nexpageNum):
            getDataProvine(passedDriver, provineName)
        else:
            ulties.writeLog("Finhish for this provine: {}".format(provineName))
        # test get first provine
        quit()
    else:
        return False


def getDataProvineReLoad(passedDriver, elementProvine, provineName):
    global refreshCount
    global currentPath
    currentPath = elementProvine.get_attribute('href')
    print(currentPath)
    # switch tab to last
    action = ActionChains(driver)
    action.move_to_element(elementProvine).key_down(Keys.CONTROL).click(
        elementProvine).key_up(Keys.CONTROL).perform()
    passedDriver.switch_to.window(passedDriver.window_handles[-1])
    quit()
    # test
    # start get data of provine
    result = getDataProvine(passedDriver, provineName)
    if(result == False):
        if(refreshCount > 0):
            refreshCount = refreshCount - 1
            wait = getRandomTime()
            ulties.writeLog("Wait {} second to reopen page provine: count {}".format(
                wait, refreshCount))
            ulties.writeLog("Reopen page provine {}".format(refreshCount))
            time.sleep(wait)
            passedDriver.close()
            passedDriver.switch_to.window(passedDriver.window_handles[-1])
            getDataProvineReLoad(passedDriver, elementProvine, provineName)


def build_driver():
    software_names = [SoftwareName.FIREFOX.value]
    operating_systems = [
        OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
    user_agent_rotator = UserAgent(
        software_names=software_names, operating_systems=operating_systems, limit=100)
    user_agent = user_agent_rotator.get_random_user_agent()
    # test for prevent block
    user_agent = "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"
    options = Options()
    # options.add_argument("--headless")
    # options.add_argument("--no-sandbox")
    # options.add_argument("--disable-gpu")
    options.add_argument(f'user-agent={user_agent}')

    profile = webdriver.FirefoxProfile()
    profile.set_preference("general.useragent.override", user_agent)
    profile.add_extension(
        extension='./extensions/touch_vpn_secure_vpn_proxy_for_unlimited_access-4.2.1-fx.xpi')
    profile.add_extension(extension='./extensions/adblock_plus-3.11-an+fx.xpi')
    profile.add_extension(
        extension='./extensions/adblock_for_firefox-4.33.0-fx.xpi')

    # API_KEY = '7f3282dc1e35451c7037fa93818b0cef'
    # proxy_options = {
    #     'proxy': {
    #         'http': f'http://scraperapi:{API_KEY}@proxy-server.scraperapi.com:8001',
    #         'https': f'http://scraperapi:{API_KEY}@proxy-server.scraperapi.com:8001',
    #         'no_proxy': 'localhost,127.0.0.1'
    #     }
    # }

    # just for test
    # firefox_binary = 'C:/Program Files/Firefox Developer Edition/firefox.exe'
    # firefox_binary = 'C:/Program Files/Mozilla Firefox/firefox.exe'

    driver = webdriver.Firefox(
        firefox_profile=profile, firefox_binary=None, options=options, seleniumwire_options=None)
    print("Agent: {}".format(user_agent))

    time.sleep(5)
    # close other tabs
    ulties.closeOtherTabs(driver)
    return driver


ulties.writeLog('start')
# seed random number generator
random.seed(time.perf_counter())
driver = build_driver()
# test
# driver.request_interceptor = interceptorRequest
currentPath = '/'
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
        provineTitle = ulties.cleanhtml(provineTitle)
        ulties.writeData("_______{}_______".format(
            provineTitle), provineTitle.replace(" ", "_"))
        # open link with new tab
        scroll_shim(driver, provine)
        # wait before open new tab
        wait = getRandomTime()
        ulties.writeLog("Wait {} second to open provine".format(wait))
        time.sleep(wait)
        refreshCount = 3
        getDataProvineReLoad(driver, provine, provineTitle.replace(" ", "_"))
        # close all tabs without first tab
        wait = getRandomTime()
        ulties.writeLog("Wait {} second to close provine tab".format(wait))
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
