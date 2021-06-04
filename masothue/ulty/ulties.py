import os
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from subprocess import Popen
import subprocess
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re

# SELENIUM_SESSION_FILE = './firefox_session'
SELENIUM_SESSION_FILE = 'firefox_session'
RUN_PATH_TIME = 0


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


def writeData(message, fileName):
    print(message)
    message = "{}\n".format(message)
    with open('{}.txt'.format(fileName), 'a',  encoding='utf-8') as the_file:
        the_file.write(message)


# @log
def build_driver(runPath):
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
            return build_driver(runPath)
    except Exception as ex:
        print('session file is not exist: {}'.format(ex))
        global RUN_PATH_TIME
        if(RUN_PATH_TIME < 1):
            runZombieBrower(runPath)
            RUN_PATH_TIME = RUN_PATH_TIME + 1
            time.sleep(20)
            return build_driver(runPath)
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

    # test add proxy for web
    PROXY = "182.160.124.26:8081"
    webdriver.DesiredCapabilities.FIREFOX['proxy'] = {
        "httpProxy": PROXY,
        "ftpProxy": PROXY,
        "sslProxy": PROXY,
        "noProxy": None,
        "proxyType": "MANUAL",
        "class": "org.openqa.selenium.Proxy",
        "autodetect": False
    }

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
