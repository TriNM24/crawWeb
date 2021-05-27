from selenium import webdriver
import os
from selenium.webdriver.firefox.options import Options
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
import ulty.ulties as ulties
import time

SELENIUM_SESSION_FILE = './firefox_session'


def build_driver():
    software_names = [SoftwareName.FIREFOX.value]
    operating_systems = [
        OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
    user_agent_rotator = UserAgent(
        software_names=software_names, operating_systems=operating_systems, limit=100)
    user_agent = user_agent_rotator.get_random_user_agent()
    options = Options()
    # options.add_argument("--headless")
    # options.add_argument("--no-sandbox")
    # options.add_argument("--window-size=1420,1080")
    # options.add_argument("--disable-gpu")
    options.add_argument(f'user-agent={user_agent}')

    profile = webdriver.FirefoxProfile()
    profile.add_extension(
        extension='./extensions/touch_vpn_secure_vpn_proxy_for_unlimited_access-4.2.1-fx.xpi')
    profile.set_preference("general.useragent.override", user_agent)
    profile.add_extension(extension='./extensions/adblock_plus-3.11-an+fx.xpi')
    profile.add_extension(
        extension='./extensions/adblock_for_firefox-4.33.0-fx.xpi')
    # just for test
    # firefox_binary = 'C:/Program Files/Firefox Developer Edition/firefox.exe'
    # firefox_binary = 'C:/Program Files/Mozilla Firefox/firefox.exe'
    driver = webdriver.Firefox(
        firefox_profile=profile, firefox_binary=None, options=options)
    # install extension
    # extension_path = r'C:\Users\nguyenminhtri\Downloads\touch_vpn_secure_vpn_proxy_for_unlimited_access-4.2.1-fx.xpi'
    # driver.install_addon(extension_path, temporary=True)

    print("Random agent: {}".format(user_agent))
    session_file = open(SELENIUM_SESSION_FILE, 'w')
    session_file.writelines([
        driver.command_executor._url,
        "\n",
        driver.session_id,
        "\n",
    ])
    time.sleep(5)
    session_file.close()
    # close other tabs
    ulties.closeOtherTabs(driver)
    return driver


print('Zombie Raised\nDo not close this screen')
driver = build_driver()
driver.get("http://google.com")
# wait input on purpose not finish this zombie brower
input()
