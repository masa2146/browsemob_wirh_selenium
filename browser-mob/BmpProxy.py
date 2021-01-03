import platform
from os.path import dirname, abspath
from browsermobproxy import Server, client
from selenium import webdriver
import time
import pprint


class ProxyManager:

    __PARENT_DIR = dirname(dirname(abspath(__file__)))
    __BMP = ''
    __system = platform.system()
    __DRIVER_PATH = ''

    if __system == 'Linux' or __system == 'Darwin':
        __BMP = __PARENT_DIR+"/browsermob-proxy-2.1.4/bin/browsermob-proxy"
        __DRIVER_PATH = __PARENT_DIR + "/drivers/chromedriver"
    elif __system == 'Windows':
        __BMP = __PARENT_DIR+"\browsermob-proxy-2.1.4\bin\browsermob-proxy.bat"

    def __init__(self):
        self.__server = Server(ProxyManager.__BMP, {'port': 9090})
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


if "__main__" == __name__:
    proxy = ProxyManager()
    server = proxy.start_server()
    client = proxy.start_client()
    client.new_har("google.com")
    print("Client Proxy: ", client.proxy)

    options = webdriver.ChromeOptions()
    options.add_argument("--proxy-server={}".format(client.proxy))
    driver = webdriver.Chrome(
        executable_path=proxy.driverPath, chrome_options=options)
    driver.get("https://www.google.com")
    time.sleep(3)
    pprint.pprint(client.har)
