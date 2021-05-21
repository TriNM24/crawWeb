from selenium import webdriver
import os

SELENIUM_SESSION_FILE = './firefox_session'


def build_driver():
    driver = webdriver.Firefox()

    session_file = open(SELENIUM_SESSION_FILE, 'w')
    session_file.writelines([
        driver.command_executor._url,
        "\n",
        driver.session_id,
        "\n",
    ])
    session_file.close()

    return driver


print('Zombie Raised\nDo not close this screen')
driver = build_driver()
driver.get("http://google.com")
# wait input on purpose not finish this zombie brower
input()
