import os
# from seleniumwire import webdriver as webdriverwire
from selenium import webdriver
from seleniumwire import webdriver as webdriverwire

from selenium.webdriver.remote.webdriver import WebDriver
from subprocess import Popen
import subprocess
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
import sys
from selenium.webdriver.firefox.options import Options
import ulties

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

from user_agent2 import (
    generate_user_agent,
)

# SELENIUM_SESSION_FILE = './firefox_session'
# SELENIUM_SESSION_FILE = 'firefox_session'
RUN_PATH_TIME = 0

sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

# 1: Danh mục câu hỏi,
# 2: Danh sách câu hỏi
def getSessionFileName(functionType):
    if(functionType == 1):
        return "DanhMucCauHoiSession"
    elif(functionType == 2):
        return "DanhSachCauHoiSession"

def log(f):
    def wrapper(*args, **kwargs):
        writeLog('start function:{}'.format(f.__name__))
        result = f(*args, **kwargs)
        writeLog('end function:{}'.format(f.__name__))
        return result
    return wrapper


def writeLog(message):
    print(message)
    message = "{}\n".format(message)
    with open('runLog.txt', 'a',  encoding='utf-8') as the_file:
        the_file.write(message)

def writeLogWithName(fileName, message):
    print(message)
    message = "{}\n".format(message)
    with open(fileName, 'a',  encoding='utf-8') as the_file:
        the_file.write(message)

def writeData(message, fileName):
    print(message)
    message = "{}\n".format(message)
    with open('{}.txt'.format(fileName), 'a',  encoding='utf-8') as the_file:
        the_file.write(message)

# @log
def build_driver(runPath, SELENIUM_SESSION_FILE):
    try:
        session_file = open(SELENIUM_SESSION_FILE)
        session_info = session_file.readlines()
        session_file.close()

        executor_url = session_info[0].strip()
        session_id = session_info[1].strip()

        driver = create_driver_session(session_id, executor_url)
        try:
            title = driver.title
            print("Success: {}".format(title))        
            return driver
        except Exception as ex:
            print("Error: {}".format(ex))
            os.remove(SELENIUM_SESSION_FILE)
            return build_driver(runPath, SELENIUM_SESSION_FILE)
    except Exception as ex:
        print('session file is not exist: {}'.format(ex))
        global RUN_PATH_TIME
        if(RUN_PATH_TIME < 1):
            runZombieBrower(runPath)
            RUN_PATH_TIME = RUN_PATH_TIME + 1
            time.sleep(20)
            return build_driver(runPath, SELENIUM_SESSION_FILE)
        else:
            quit()


def create_driver_session(session_id, executor_url):
    from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver

    # Save the original function, so we can revert our patch
    org_command_execute = RemoteWebDriver.execute

    def new_command_execute(self, command, params=None):
        if command == "newSession":
            # Mock the response
            return {'success': 0, 'value': None, 'sessionId': session_id}
        else:
            return org_command_execute(self, command, params)

    # Patch the function before creating the driver object
    RemoteWebDriver.execute = new_command_execute

    new_driver = webdriver.Remote(
        command_executor=executor_url, desired_capabilities=webdriver.DesiredCapabilities.FIREFOX)
    new_driver.session_id = session_id

    # Replace the patched function with original function
    RemoteWebDriver.execute = org_command_execute

    return new_driver


def runZombieBrower(file_path):
    Popen(file_path, creationflags=subprocess.CREATE_NEW_CONSOLE)


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


def closeOtherTabs(passedDriver):
    firstTime = True
    for handle in passedDriver.window_handles:
        passedDriver.switch_to.window(handle)
        if(not firstTime):
            passedDriver.close()
        firstTime = False
    passedDriver.switch_to.window(passedDriver.window_handles[0])

def build_driver():
    try:
        try:           
            user_agent = generate_user_agent(navigator="firefox")
        except Exception as ex:
            print("UserAgent have error {}".format(ex))

        options = Options()
        options.add_argument(f'user-agent={user_agent}')
        profile = webdriver.FirefoxProfile()
        profile.set_preference('intl.accept_languages', 'en-US, en')
        profile.set_preference("general.useragent.override", user_agent)
        driver = webdriver.Firefox(firefox_profile=profile, options=options)

        print("Random agent: {}".format(user_agent))
        time.sleep(5)
        # close other tabs
        ulties.closeOtherTabs(driver)
        return driver
    except Exception as ex:
        print("aaaaaaaaaaa:{}".format(ex))

def build_driver2():
    try:
        
        # profile = webdriver.FirefoxProfile('C:/Users/Administrator/AppData/Roaming/Mozilla/Firefox/Profiles/msmpjo8k.default-esr')
        profile = webdriver.FirefoxProfile('C:/Users/downloadman/AppData/Roaming/Mozilla/Firefox/Profiles/be4a7255.default-release')
        profile.set_preference("dom.webdriver.enabled", False)
        profile.set_preference('useAutomationExtension', False)
        profile.set_preference('intl.accept_languages', 'en-US, en')

        # options = Options()
        # options.add_argument("start-maximized")
        # options.add_argument("disable-infobars")
        # options.add_argument("--disable-extensions")
        # options.add_argument('--no-sandbox')
        # options.add_argument('--disable-application-cache')
        # options.add_argument('--disable-gpu')
        # options.add_argument("--disable-dev-shm-usage")
        
        profile.update_preferences()
        desired = DesiredCapabilities.FIREFOX
        driver = webdriver.Firefox(firefox_profile=profile,desired_capabilities=desired)
        # close other tabs
        ulties.closeOtherTabs(driver)
        return driver
    except Exception as ex:
        writeLog('Error while build_driver2:{}'.format(ex))

def build_driverwire():
    try:
        
        # profile = webdriver.FirefoxProfile('C:/Users/Administrator/AppData/Roaming/Mozilla/Firefox/Profiles/msmpjo8k.default-esr')
        profile = webdriverwire.FirefoxProfile('C:/Users/downloadman/AppData/Roaming/Mozilla/Firefox/Profiles/be4a7255.default-release')
        profile.set_preference("dom.webdriver.enabled", False)
        profile.set_preference('useAutomationExtension', False)
        profile.set_preference('intl.accept_languages', 'en-US, en')

        # options = Options()
        # options.add_argument("start-maximized")
        # options.add_argument("disable-infobars")
        # options.add_argument("--disable-extensions")
        # options.add_argument('--no-sandbox')
        # options.add_argument('--disable-application-cache')
        # options.add_argument('--disable-gpu')
        # options.add_argument("--disable-dev-shm-usage")
        
        profile.update_preferences()
        desired = DesiredCapabilities.FIREFOX
        driver = webdriverwire.Firefox(firefox_profile=profile,desired_capabilities=desired)
        # close other tabs
        ulties.closeOtherTabs(driver)
        return driver
    except Exception as ex:
        writeLog('Error while build_driver2:{}'.format(ex))

def getRealNumber(numberString):

    # remove 'khác' in string
    numberString = numberString.replace('khác','')
    numberString = numberString.replace('Likes','')

    #pre process
    #"Vũ Trần Kim Nhã và 2.2M người khác
    m = re.search(r"\d", numberString)    
    if m:        
        numberString = numberString[m.start():len(numberString)]
        #2.2M người khác
        m = re.search(r"[kKMm]",numberString)
        if m:            
            temp = m.start()
            if(temp > 0 and temp < 5):
                numberString = numberString[0:temp+1]
                #2.2M

    # print(numberString)

    if('triệu' in numberString):
        if(',' in numberString or '.' in numberString):
            numberString = numberString.replace('triệu','00000')
        else:
            testString = numberString.replace('triệu','000000')
    elif('k' in numberString or 'K' in numberString):
        if(',' in numberString or '.' in numberString):
            numberString = numberString.replace('k','00')
            numberString = numberString.replace('K','00')
        else:
            numberString = numberString.replace('k','000')
            numberString = numberString.replace('K','000')
    elif('m' in numberString or 'M' in numberString):
        if(',' in numberString or '.' in numberString):
            numberString = numberString.replace('m','00000')
            numberString = numberString.replace('M','00000')
        else:
            numberString = numberString.replace('m','000000')
            numberString = numberString.replace('M','000000')

    intString = re.sub(r'[^0-9]',r'',numberString)
    return intString

def build_driver_chrome() -> WebDriver:
    try:
        options = webdriver.ChromeOptions()
        options.add_argument(r"user-data-dir=C:\Users\Administrator\AppData\Local\Google\Chrome\User Data")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # options.add_argument(r'--profile-directory=	C:\Users\downloadman\AppData\Local\Google\Chrome\User Data\Default')
        driver = webdriver.Chrome(executable_path=r'C:\Users\Administrator\AppData\Local\Programs\Python\Python310\Tools\chromedriver.exe', chrome_options=options)
        return driver
    except Exception as ex:
        writeLog('Error while build_driver_chrome:{}'.format(ex))   
