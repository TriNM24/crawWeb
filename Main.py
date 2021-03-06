import sys
from selenium import webdriver
import LoginAccount
import pickle
# import loginaccount as login
# set endcoding
sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')
driver = webdriver.Firefox()
# init domain
driver.get("https://www.facebook.com/")
try:
    cookies = pickle.load(open("cookies.pkl", "rb"))
    driver.delete_all_cookies()
    for cookie in cookies:
        driver.add_cookie(cookie)
    print('Load cookies successfully')
except Exception as e:
    print("Can not load cookies " + str(e))
# reload to login via cookies
driver.get("https://www.facebook.com/")

if 'đăng nhập' in driver.title.lower() or 'log in' in driver.title.lower():
    print('Login')
    LoginAccount.loginFace(driver)
else:
    print('Allready login')
executor_url = driver.command_executor._url
session_id = driver.session_id
print("executor_url:{}".format(executor_url))
print("session_id:{}".format(session_id))
#LoginAccount.getDataFace(driver)

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

    new_driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
    new_driver.session_id = session_id

    # Replace the patched function with original function
    RemoteWebDriver.execute = org_command_execute

    return new_driver

driver2 = create_driver_session(session_id, executor_url)
# driver2.get("http://www.mrsmart.in")
print(driver2.current_url)
driver.close()
