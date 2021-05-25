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
    scroll_by_coord = 'window.scrollTo(%s,%s);' % (x,y)
    scroll_nav_out_of_way = 'window.scrollBy(0, -120);'
    passed_in_driver.execute_script(scroll_by_coord)
    passed_in_driver.execute_script(scroll_nav_out_of_way)

print('start')
driver = ulties.build_driver()
driver.get('https://masothue.com/')
xpathProvines = "//ul[@class='row']"
element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, xpathProvines)))
provines = element.find_elements_by_xpath("./li/a")
# for provine in provines:
#     print(provine.get_attribute('innerHTML'))
# testt
scroll_shim(driver, provines[0])
print(provines[0].get_attribute('innerHTML'))
action = ActionChains(driver)
action.move_to_element(provines[0])
provines[0].click()

# get data
print(driver.title)
xpathData = "//div[@class='tax-listing']"
element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, xpathData)))
scroll_shim(driver, element)
companies = element.find_elements_by_xpath("./div")
# test company 1
# print(companies[0].get_attribute('innerHTML'))
for company in companies:
    title = company.find_element_by_xpath("./h3/a").get_attribute('innerHTML')
    taxNumber = company.find_element_by_xpath("./div/a").get_attribute('innerHTML')
    owner = company.find_element_by_xpath("./div/em/a").get_attribute('innerHTML')
    address = company.find_element_by_xpath("./address").get_attribute('innerHTML')
    addressResult = address[address.find("/i>")+3:].strip()
    print(title)
    print(taxNumber)
    print(owner)
    print(address)
    ulties.writeLog("{}\n{}\n{}\n{}".format(title,taxNumber,owner,addressResult))

# move to next page
print("____________next page____________")
xpathPageNumber = "//ul[@class='page-numbers']"
element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, xpathPageNumber)))
scroll_shim(driver, element)
pages = element.find_elements_by_xpath("./li")
isHaveCurrent = False
for page in pages:
    if(isHaveCurrent==False):
        try:
            page.find_element_by_xpath("./span")
            isHaveCurrent = True
        except Exception as ex:
            sHaveCurrent = False
    else:
        #move to next page
        page.find_element_by_xpath("./a").click()
        break



quit()