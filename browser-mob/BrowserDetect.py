import platform
from os.path import dirname, abspath
import  urllib.request
import urllib
from zipfile import ZipFile
import webbrowser


class DetectManager:

    __BROWSER_LIST = ['google-chrome', 'chrome', 'chromium',
                      'chromium-browser', 'mozilla', 'firefox']
    __defaultBrowser = ''
    __PARENT_DIR = dirname(dirname(abspath(__file__)))

    def detectBrowser(self):
        """Detect able to browser in system.

        Returns:
            [str]: [description]
        """
        for browser in self.__BROWSER_LIST:
            try:
                self.__defaultBrowser = webbrowser.get(browser).name
                break
            except Exception:
                continue
        return self.__defaultBrowser

    def __downloadDriver(self):
        if self.__defaultBrowser == 'google-chrome' or self.__defaultBrowser == 'chrome' \
                or self.__defaultBrowser == 'chromium' or self.__defaultBrowser == 'chromium-browser':
            self.__downloadChromeDriver()
        elif self.__defaultBrowser == 'mozilla' or self.__defaultBrowser == 'firefox':
            self.__downloadGeckoDriver()

    def __downloadChromeDriver(self):

        chromeVersion = self.__getChromeVersion()
        downloadLink = 'https://chromedriver.storage.googleapis.com/index.html?path='+chromeVersion
        if platform.system() == 'Linux':
            self.__download(
                downloadLink+"/chromedriver_linux64.zip", self.__PARENT_DIR+"/drivers")
        elif platform.system() == 'Darwin':
            self.__download(
                downloadLink+"/chromedriver_mac64.zip", self.__PARENT_DIR+"/drivers")
        elif platform.system() == 'Windows':
            self.__download(
                downloadLink+"/chromedriver_win32.zip", self.__PARENT_DIR+"/drivers")

    def __getChromeVersion(self):
        x = urllib.request.urlopen(
            'https://chromedriver.storage.googleapis.com/LATEST_RELEASE')
        return x.read()

    def __downloadGeckoDriver(self):
        systemName = platform.system()
        arch = platform.architecture()[0]
        downloadLink = 'https://github.com/mozilla/geckodriver/releases/download/v0.28.0/'
        if systemName == 'Linux':
            if arch == '32bit':
                self.__download(downloadLink+"geckodriver-v0.28.0-linux32.tar.gz")
            elif arch == '64bit':
                self.__download(downloadLink+"geckodriver-v0.28.0-linux64.tar.gz")
        if systemName == 'Darwin':
                self.__download(downloadLink+"geckodriver-v0.28.0-macos.tar.gz")
        if systemName == 'Windows':
            if arch == '32bit':
                file = self.__download(downloadLink+"geckodriver-v0.28.0-win32.zip")
                self.__unzip(file)
            elif arch == '64bit':
                file = self.__download(downloadLink+"geckodriver-v0.28.0-win64.zip")
                self.__unzip(file)

    def __download(self, url):
        return urllib.request.urlopen(url)

    def __unzip(self,file):
        tempzip = open(self.__PARENT_DIR+"/drivers/temp.zip", "wb")
        tempzip.write(file.read())
        tempzip.close()
        zf = ZipFile(tempzip.name)
        zf.extractall(path = self.__PARENT_DIR+"/drivers/")
        zf.close()

    def __untar(self,file):
        pass
    



if __name__ == "__main__":
    detect = DetectManager()
    print(detect.detectBrowser())
