from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


class Request:
    selenium_retries = 0

    def __init__(self, url):
        self.url = url

    def get_selenium_res(self, class_name):
        try:
            software_names = [SoftwareName.FIREFOX.value]
            operating_systems = [
                OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
            user_agent_rotator = UserAgent(
                software_names=software_names, operating_systems=operating_systems, limit=100)
            # Get Random User Agent String.
            user_agent = user_agent_rotator.get_random_user_agent()
            options = Options()
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--window-size=1420,1080")
            options.add_argument("--disable-gpu")
            options.add_argument(f'user-agent={user_agent}')
            browser = webdriver.Firefox(options=options)
            # when testing proxies
            browser.get(self.url)
            print(browser.title)
        except Exception as ex:
            print(ex)
