# see rkengler.com for related blog post
# https://www.rkengler.com/how-to-capture-network-traffic-when-scraping-with-selenium-and-python/

import json
import pprint
import  sys
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


from os.path import dirname, abspath
__PARENT_DIR = dirname(dirname(abspath(__file__)))

sys.path.insert(1, __PARENT_DIR+'/browser-mob')
from BmpProxy import ProxyManager

proxy = ProxyManager()
server = proxy.start_server()
client = proxy.start_client()
proxy.selectBrowser(ProxyManager.FIREFOX)
client.new_har("google.com")

options = webdriver.ChromeOptions()
options.add_argument("--proxy-server={}".format(client.proxy))
options.add_argument("--enable-javascript")
options.add_argument("user-data-dir=selenium")
options.add_argument('ignore-certificate-errors')

capabilities = DesiredCapabilities.CHROME
# capabilities["loggingPrefs"] = {"performance": "ALL"}  # chromedriver < ~75
capabilities["goog:loggingPrefs"] = {"performance": "ALL"}  # chromedriver 75+

driver = webdriver.Chrome(
    __PARENT_DIR+"/drivers/chromedriver",
    desired_capabilities=capabilities,
    chrome_options=options
)


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


driver.get("https://giris.hepsiburada.com/?ReturnUrl=https%3A%2F%2Foauth.hepsiburada.com%2Fconnect%2Fauthorize%2Fcallback%3Fclient_id%3DSPA%26redirect_uri%3Dhttps%253A%252F%252Fwww.hepsiburada.com%252Fuyelik%252Fcallback%26response_type%3Dcode%26scope%3Dopenid%2520profile%26state%3D80f83f90fdac4e12b0ea3f43ec6a47cf%26code_challenge%3D-ExPwARL4RXYAnOMfW1fchyLrkCVm1bSZZqxxB6d1DY%26code_challenge_method%3DS256%26response_mode%3Dquery")

# logs = driver.get_log("performance")

# events = process_browser_logs_for_network_events(logs)
# print(events)
# with open("log_entries.json", "wt") as out:
#     for event in events:
#         pprint.pprint(event, stream=out)