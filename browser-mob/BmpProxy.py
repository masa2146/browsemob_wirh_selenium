import platform
from os.path import dirname, abspath
from browsermobproxy import Server, client
from selenium import webdriver
import time
import pprint
from BrowserDetect import DetectManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class ProxyManager:
    """
    Detect http request via proxy.

    Returns:
        [type]: [description]
    """
    __PARENT_DIR = dirname(dirname(abspath(__file__)))
    __OS_NAME = platform.system()
    __DRIVER_PATH = ''

    GOOGLE_CHROME = "google-chrome"
    CHROME = "chrome"
    CHROMIUM = "chromium"
    CHROMIUM_BROWSER = "chromium-browser"
    MOZILLA = "mozilla"
    FIREFOX = "firefox"

    detectManager = DetectManager()

    def __init__(self):
        self.detectManager.createDriver()
        if ProxyManager.__OS_NAME == 'Linux' or ProxyManager.__OS_NAME == 'Darwin':
            self.__BMP = self.__PARENT_DIR+"/browsermob-proxy-2.1.4/bin/browsermob-proxy"
            self.__DRIVER_PATH = self.__PARENT_DIR + "/drivers/" + self.__getDriverName('')
        elif ProxyManager.__OS_NAME == 'Windows':
            self.__BMP = self.__PARENT_DIR+"\browsermob-proxy-2.1.4\bin\browsermob-proxy.bat"

        self.__server = Server(self.__BMP, {'port': 9090})
        self.__client = None

    def start_server(self):
        self.__server.start()
        return self.__server

    def start_client(self):
        self.__client = self.__server.create_proxy(
            params={"trustAllServer": "true"})
        return self.__client

    @property
    def client(self):
        return self.__client

    @property
    def server(self):
        return self.__server

    @property
    def driverPath(self):
        return self.__DRIVER_PATH

    def selectBrowser(self, browserName):
        self.__DRIVER_PATH = self.__PARENT_DIR + "/drivers/" + self.__getDriverName(browserName)

    def __getDriverName(self,browserName):
        """
        If selected value is None or is empty then get driver  of the first installed browser.
        Else get driver of the selected browser.  
        """
        if browserName is None or browserName == '':
            return next(iter(self.detectManager.installedBrowser.values()))
        else:
            return self.detectManager.installedBrowser[browserName]


if "__main__" == __name__:
    proxy = ProxyManager()
    server = proxy.start_server()
    client = proxy.start_client()
    proxy.selectBrowser(ProxyManager.CHROMIUM_BROWSER)
    client.new_har("google.com")
    print("Client Proxy: ", client.proxy)

    capabilities = DesiredCapabilities.CHROME
    capabilities["goog:loggingPrefs"] = {"performance": "ALL"}

    options = webdriver.ChromeOptions()
    options.add_argument("--proxy-server={}".format(client.proxy))
    options.add_argument("--enable-javascript")
    options.add_argument("user-data-dir=selenium")
    options.add_argument('ignore-certificate-errors')
    driver = webdriver.Chrome(
        executable_path=proxy.driverPath, chrome_options=options)
    driver.get("https://giris.hepsiburada.com/?ReturnUrl=https%3A%2F%2Foauth.hepsiburada.com%2Fconnect%2Fauthorize%2Fcallback%3Fclient_id%3DSPA%26redirect_uri%3Dhttps%253A%252F%252Fwww.hepsiburada.com%252Fuyelik%252Fcallback%26response_type%3Dcode%26scope%3Dopenid%2520profile%26state%3D80f83f90fdac4e12b0ea3f43ec6a47cf%26code_challenge%3D-ExPwARL4RXYAnOMfW1fchyLrkCVm1bSZZqxxB6d1DY%26code_challenge_method%3DS256%26response_mode%3Dquery")
    time.sleep(3)
    pprint.pprint(client.har)

## FIREFOX

    # options = webdriver.FirefoxOptions()
    # options.add_argument("--proxy-server={}".format(client.proxy))
    # options.add_argument("--enable-javascript")
    # options.add_argument("user-data-dir=selenium")

    # driver = webdriver.Firefox(
    #     executable_path=proxy.driverPath, options=options, desired_capabilities=capabilities)
    # driver.get("https://giris.hepsiburada.com/?ReturnUrl=https%3A%2F%2Foauth.hepsiburada.com%2Fconnect%2Fauthorize%2Fcallback%3Fclient_id%3DSPA%26redirect_uri%3Dhttps%253A%252F%252Fwww.hepsiburada.com%252Fuyelik%252Fcallback%26response_type%3Dcode%26scope%3Dopenid%2520profile%26state%3D80f83f90fdac4e12b0ea3f43ec6a47cf%26code_challenge%3D-ExPwARL4RXYAnOMfW1fchyLrkCVm1bSZZqxxB6d1DY%26code_challenge_method%3DS256%26response_mode%3Dquery")
    # time.sleep(3)
    # pprint.pprint(client.har)
