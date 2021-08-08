from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.firefox.options import Options
import time


def createFirefox():
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"
    try:
        ua = UserAgent()
        user_agent = ua.firefox
        # update saved database
        # ua.update()
    except Exception as ex:
        print("UserAgent have error {}".format(ex))
    print(user_agent)
    options = Options()
    # options.add_argument("--headless")
    # options.add_argument("--no-sandbox")
    # options.add_argument("--window-size=1420,1080")
    # options.add_argument("--disable-gpu")
    options.add_argument(f'user-agent={user_agent}')
    profile = webdriver.FirefoxProfile()
    profile.set_preference('intl.accept_languages', 'en-US, en')
    profile.set_preference("general.useragent.override", user_agent)
    profile.add_extension(
        extension='./extensions/touch_vpn_secure_vpn_proxy_for_unlimited_access-4.2.1-fx.xpi')
    profile.add_extension(extension='./extensions/adblock_plus-3.11-an+fx.xpi')
    profile.add_extension(
        extension='./extensions/adblock_for_firefox-4.33.0-fx.xpi')

    driver = webdriver.Firefox(
        firefox_profile=profile, firefox_binary=None, options=options)
    time.sleep(15)
    closeOtherTabs(driver)
    return driver


def closeOtherTabs(passedDriver):
    firstTime = True
    for handle in passedDriver.window_handles:
        passedDriver.switch_to.window(handle)
        if(not firstTime):
            passedDriver.close()
        firstTime = False
    passedDriver.switch_to.window(passedDriver.window_handles[0])
