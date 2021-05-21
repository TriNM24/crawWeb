import os
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from subprocess import Popen
import subprocess
import time

SELENIUM_SESSION_FILE = './firefox_session'


def optional_arg_decorator(fn):
    print('hey log start')

    def wrapped_decorator(*args):
        if len(args) == 1 and callable(args[0]):
            return fn(args[0])

        else:
            def real_decorator(decoratee):
                return fn(decoratee, *args)

            return real_decorator

    print('hey log end')
    return wrapped_decorator


def log(f):
    def wrapper(*args, **kwargs):
        print('hey log start')
        f(*args, **kwargs)
        print('hey log end')
    return wrapper


def log2(f):
    def wrapper(*args, **kwargs):
        with open('somefile.txt', 'a') as the_file:
            the_file.write('start function:{}\n'.format(f.__name__))
        print('start function:{}'.format(f.__name__))
        result = f(*args, **kwargs)
        print('end function:{}'.format(f.__name__))
        with open('somefile.txt', 'a') as the_file:
            the_file.write('end function:{}\n'.format(f.__name__))
        return result
    return wrapper


@log2
def build_driver():
    if os.path.isfile(SELENIUM_SESSION_FILE):
        session_file = open(SELENIUM_SESSION_FILE)
        session_info = session_file.readlines()
        session_file.close()

        executor_url = session_info[0].strip()
        session_id = session_info[1].strip()

        driver = create_driver_session(session_id, executor_url)
        try:
            title = driver.title
            print("Success")
            return driver
        except Exception as ex:
            print("Error")
            os.remove(SELENIUM_SESSION_FILE)
            return build_driver()
    else:
        print('session file is not exist.')
        runZombieBrower('runzombi.bat')
        time.sleep(20)
        return build_driver()


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
        command_executor=executor_url, desired_capabilities={})
    new_driver.session_id = session_id

    # Replace the patched function with original function
    RemoteWebDriver.execute = org_command_execute

    return new_driver


def runZombieBrower(file_path):
    Popen(file_path, creationflags=subprocess.CREATE_NEW_CONSOLE)
