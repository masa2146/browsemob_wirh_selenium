import contextlib
from selenium import webdriver
from os.path import dirname, abspath
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import sys
import time

__PARENT_DIR = dirname(dirname(abspath(__file__)))
sys.path.insert(1, __PARENT_DIR+'/browser-mob')
from BmpProxy import ProxyManager


@contextlib.contextmanager
def browser_and_proxy():
    proxy = ProxyManager()
    server = proxy.start_server()
    client = proxy.start_client()
    proxy.selectBrowser(ProxyManager.CHROME)
    client.new_har(options={'captureContent': True})
    # Set up Chrome
    option = webdriver.ChromeOptions()
    option.add_argument('--proxy-server=%s' % client.proxy)

    prefs = {"profile.managed_default_content_settings.images": 2}
    option.add_experimental_option("prefs", prefs)
    option.add_argument('ignore-certificate-errors')
    # option.add_argument('--headless')
    # option.add_argument('--no-sandbox')
    # option.add_argument('--disable-gpu')

    capabilities = DesiredCapabilities.CHROME.copy()
    capabilities['acceptSslCerts'] = True
    capabilities['acceptInsecureCerts'] = True

    browser = webdriver.Chrome(options=option,
                            desired_capabilities=capabilities,
                            executable_path=proxy.driverPath)

    try:
        yield browser, client
    finally:
        browser.quit()
        server.stop()

def scan_and_block_har(proxy):
    all_requests_finished = False
    while all_requests_finished is False:
        all_requests_finished = True
        for e in proxy.har['log']['entries']:
            if 'explore_tabs' in e['request']['url']:
                if e['response']['status'] != 200 or e['response']['content'].get('text') is None:
                    all_requests_finished = False
    return

def scan_har(proxy):
    print(proxy.har)
    for e in proxy.har['log']['entries']:
        if 'explore_tabs' in e['request']['url']:
            print('Request URL: {}'.format(e['request']['url']))
            print('Status: {}'.format(e['response']['status']))

def demo():
    with browser_and_proxy() as (driver, proxy):
        driver.get('https://giris.hepsiburada.com/?ReturnUrl=https%3A%2F%2Foauth.hepsiburada.com%2Fconnect%2Fauthorize%2Fcallback%3Fclient_id%3DSPA%26redirect_uri%3Dhttps%253A%252F%252Fwww.hepsiburada.com%252Fuyelik%252Fcallback%26response_type%3Dcode%26scope%3Dopenid%2520profile%26state%3D6ca36281c816438eb6fa68aa5d7e06ce%26code_challenge%3DhyOEDMixtGUXPMsQ7cBV4Kvgcp7r6kqu1MqFOmaAdSg%26code_challenge_method%3DS256%26response_mode%3Dquery')
        time.sleep(3)
        scan_and_block_har(proxy)
        scan_har(proxy)
        registerSwitch = driver.find_elements_by_xpath('//div[@class="_2q4oJzGUsyLIOBhRdWWO9D"]')
        registerSwitch[1].click()

        firstName = driver.find_element_by_xpath('//input[@name="firstName"]')
        lastName = driver.find_element_by_xpath('//input[@name="lastName"]')
        mail = driver.find_element_by_xpath('//input[@name="email"]')
        password = driver.find_element_by_xpath('//input[@name="password"]')
        submit = driver.find_element_by_xpath('//button[@name="btnSignUpSubmit"]')

        firstName.send_keys('Asid')
        lastName.send_keys('Cesmi')
        mail.send_keys('fatihbulut1000456@hotmail.com')
        password.send_keys('sdaA123.')
        submit.click()
        time.sleep(10)
        scan_and_block_har(proxy)
        scan_har(proxy)


if __name__ == '__main__':
    demo()
