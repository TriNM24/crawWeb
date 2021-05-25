from selenium import webdriver
import os
from selenium.webdriver.firefox.options import Options
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

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
    driver = webdriver.Firefox(options=options)

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
