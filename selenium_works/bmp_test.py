import json
import pprint
import sys
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import time

from os.path import dirname, abspath
__PARENT_DIR = dirname(dirname(abspath(__file__)))

sys.path.insert(1, __PARENT_DIR+'/browser-mob')
from BmpProxy import ProxyManager


def process_browser_logs_for_network_events(logs):
    """
    Return only logs which have a method that start with "Network.response", "Network.request", or "Network.webSocket"
    since we're interested in the network events specifically.
    """
    for entry in logs:
        log = json.loads(entry["message"])["message"]
        if (
                "Network.response" in log["method"]
                or "Network.request" in log["method"]
                or "Network.webSocket" in log["method"]
        ):
            yield log

proxy = ProxyManager()
# server = proxy.start_server()
# client = proxy.start_client()
# proxy.selectBrowser(ProxyManager.CHROMIUM_BROWSER)
# client.new_har("hepsiburada-register.com")
# print("Client Proxy: ", client.proxy)

capabilities = DesiredCapabilities.CHROME
capabilities["goog:loggingPrefs"] = {"performance": "ALL"}

options = webdriver.ChromeOptions()
# options.add_argument("--proxy-server={}".format(client.proxy))
options.add_argument("--enable-javascript")
options.add_argument("user-data-dir=selenium")
options.add_argument('ignore-certificate-errors')
driver = webdriver.Chrome(
    executable_path=proxy.driverPath, chrome_options=options)
driver.get("https://giris.hepsiburada.com/?ReturnUrl=https%3A%2F%2Foauth.hepsiburada.com%2Fconnect%2Fauthorize%2Fcallback%3Fclient_id%3DSPA%26redirect_uri%3Dhttps%253A%252F%252Fwww.hepsiburada.com%252Fuyelik%252Fcallback%26response_type%3Dcode%26scope%3Dopenid%2520profile%26state%3D6ca36281c816438eb6fa68aa5d7e06ce%26code_challenge%3DhyOEDMixtGUXPMsQ7cBV4Kvgcp7r6kqu1MqFOmaAdSg%26code_challenge_method%3DS256%26response_mode%3Dquery")
# driver.maximize_window()

time.sleep(3)
registerSwitch = driver.find_elements_by_xpath('//div[@class="_2q4oJzGUsyLIOBhRdWWO9D"]')
registerSwitch[1].click()

firstName = driver.find_element_by_xpath('//input[@name="firstName"]') 
lastName = driver.find_element_by_xpath('//input[@name="lastName"]') 
mail = driver.find_element_by_xpath('//input[@name="email"]') 
password = driver.find_element_by_xpath('//input[@name="password"]') 
submit = driver.find_element_by_xpath('//button[@name="btnSignUpSubmit"]') 

firstName.send_keys('Fatih')
lastName.send_keys('Bulut')
mail.send_keys('fatihbulut10003@hotmail.com')
password.send_keys('sdaA123.')
submit.click()

logs = driver.get_log("performance")

events = process_browser_logs_for_network_events(logs)
print(events)
with open("hepsiburada.json", "wt") as out:
    for event in events:
        pprint.pprint(event, stream=out)

# time.sleep(15)
# pprint.pprint(client.har)
