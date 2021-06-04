from seleniumwire import webdriver
import os
from selenium.webdriver.firefox.options import Options
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
import ulty.ulties as ulties
import time

SELENIUM_SESSION_FILE = './firefox_session'


def interceptor(request):
    abord_list = ['/analytics-track', '/ads-track',
                  '/social-track', '/assets', '/gtag']
    # Block PNG, JPEG and GIF images
    if request.path.endswith(('.png', '.jpg', '.gif', '.ttf', 'woff', '.woff2', '.ico', 'adsbygoogle.js', '/ads',
                              '/analytics.js', '/notification.json', '/Token')):
        request.abort()
    elif(any(abord for abord in abord_list if(abord in request.path))):
        print("___Abord Request :{}".format(request.path))
        request.abort()
    else:
        print("Request :{}".format(request.path))


def interceptorDetail(request):
    abord_list = ['/analytics-track', '/ads-track',
                  '/social-track', '/assets', '/gtag']
    # Block PNG, JPEG and GIF images
    if request.path.endswith(('.png', '.jpg', '.gif', '.ttf', 'woff', '.woff2', '.ico', 'adsbygoogle.js', '/ads',
                              '/analytics.js', '/notification.json', '/Token')):
        request.abort()
    elif(any(abord for abord in abord_list if(abord in request.path))):
        print("___Abord Request :{}".format(request.path))
        request.abort()
    else:
        print("Request :{}".format(request.path))


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
    firefox_binary = 'C:/Program Files/Firefox Developer Edition/firefox.exe'
    # firefox_binary = 'C:/Program Files/Mozilla Firefox/firefox.exe'

    driver = webdriver.Firefox(
        firefox_profile=profile, firefox_binary=firefox_binary, options=options, seleniumwire_options=None)

    print("Agent: {}".format(user_agent))
    session_file = open(SELENIUM_SESSION_FILE, 'w')
    session_file.writelines([
        driver.command_executor._url,
        "\n",
        driver.session_id,
        "\n",
    ])
    session_file.close()
    time.sleep(5)
    # close other tabs
    ulties.closeOtherTabs(driver)
    return driver


print('Zombie Raised\nDo not close this screen')
driver = build_driver()
driver.request_interceptor = interceptor
print("Start done")
input()
driver.quit()
