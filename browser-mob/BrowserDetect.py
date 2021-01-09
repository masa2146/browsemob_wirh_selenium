import platform
import os
from os.path import dirname, abspath
from os.path import basename
from os import path
import requests
from zipfile import ZipFile
import tarfile
import webbrowser
import sys


class DetectManager:

    __BROWSER_LIST = ['google-chrome', 'chrome', 'chromium',
                      'chromium-browser', 'mozilla', 'firefox']
    __PARENT_DIR = dirname(dirname(abspath(__file__)))
    __installedBrowser = {}

    @property
    def installedBrowser(self):
        return self.__installedBrowser

    def createDriver(self):
        """Detect able to browser in system.

        Returns:
            [str]: [description]
        """
        for browser in self.__BROWSER_LIST:
            try:
                browserName = webbrowser.get(browser).name
                isExists, driverName = self.__checkDriver(browserName)
                if isExists is False:
                    self.__downloadDriver(browserName)
                self.__installedBrowser[browserName] = driverName    
            except Exception:
                continue

    def __checkDriver(self, browserName):
        if browserName == 'google-chrome' or browserName == 'chrome' \
                or browserName == 'chromium' or browserName == 'chromium-browser':
            if path.exists(self.__PARENT_DIR+"/drivers/chromedriver") is False:
                return False, None
            else:
                return True, 'chromedriver'
        elif browserName == 'mozilla' or browserName == 'firefox':
            if path.exists(self.__PARENT_DIR+"/drivers/geckodriver") is False:
                return False, None
            else:
                return True, 'geckodriver'

    def __downloadDriver(self, browserName):
        if browserName == 'google-chrome' or browserName == 'chrome' \
                or browserName == 'chromium' or browserName == 'chromium-browser':
            self.__downloadChromeDriver()
        elif browserName == 'mozilla' or browserName == 'firefox':
            self.__downloadGeckoDriver()

    def __downloadChromeDriver(self):

        chromeVersion = self.__getChromeVersion()
        downloadLink = 'https://chromedriver.storage.googleapis.com/'+chromeVersion
        if platform.system() == 'Linux':
            self.__download(
                downloadLink+"/chromedriver_linux64.zip")
        elif platform.system() == 'Darwin':
            self.__download(
                downloadLink+"/chromedriver_mac64.zip")
        elif platform.system() == 'Windows':
            self.__download(
                downloadLink+"/chromedriver_win32.zip")

    def __getChromeVersion(self):
        return requests.get('https://chromedriver.storage.googleapis.com/LATEST_RELEASE').content.decode('UTF-8')

    def __downloadGeckoDriver(self):
        systemName = platform.system()
        arch = platform.architecture()[0]
        downloadLink = 'https://github.com/mozilla/geckodriver/releases/download/v0.28.0/'
        if systemName == 'Linux':
            if arch == '32bit':
                self.__download(
                    downloadLink+"geckodriver-v0.28.0-linux32.tar.gz")
            elif arch == '64bit':
                self.__download(
                    downloadLink+"geckodriver-v0.28.0-linux64.tar.gz")
        if systemName == 'Darwin':
            self.__download(downloadLink+"geckodriver-v0.28.0-macos.tar.gz")
        if systemName == 'Windows':
            if arch == '32bit':
                file = self.__download(
                    downloadLink+"geckodriver-v0.28.0-win32.zip")
                self.__unzip(file)
            elif arch == '64bit':
                file = self.__download(
                    downloadLink+"geckodriver-v0.28.0-win64.zip")
                self.__unzip(file)

    def __download(self, url):
        print("Download URL: ", url)
        fileName = basename(url)
        baseName, file_extension = os.path.splitext(fileName)
        with open(fileName, 'wb') as f:
            response = requests.get(url, stream=True)
            total = response.headers.get('content-length')
            print('[*] Downloading {} file of size {:.2f} MB...'.format(baseName,
                                                                        int(total)/(1024*1024)))
            if total is None:
                f.write(response.content)
            else:
                downloaded = 0
                total = int(total)
                for data in response.iter_content(chunk_size=max(int(total/1000), 1024*1024)):
                    downloaded += len(data)
                    f.write(data)
                    done = int(50*downloaded/total)
                    sys.stdout.write('\r[{}{}]'.format(
                        '█' * done, '.' * (50-done)))
                    sys.stdout.flush()
        sys.stdout.write('\n')
        print('[*] Done!')

        if file_extension == '.tar' or file_extension == '.gz':
            self.__untar(fileName)
        elif file_extension == '.zip':
            self.__unzip(fileName)

    def __untar(self, file):
        if file.endswith("tar.gz"):
            tar = tarfile.open(file, "r:gz")
            tar.extractall(path=self.__PARENT_DIR+"/drivers/")
            tar.close()
        elif file.endswith("tar"):
            tar = tarfile.open(file, "r:")
            tar.extractall(path=self.__PARENT_DIR+"/drivers/")
            tar.close()
        os.remove(file)

    def __unzip(self, file):
        zf = ZipFile(file)
        zf.extractall(path=self.__PARENT_DIR+"/drivers/")
        zf.close()
        os.remove(file)
