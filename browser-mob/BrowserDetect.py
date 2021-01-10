import platform
from os.path import dirname, abspath
from os.path import basename
from os import path
import  urllib.request
import urllib
import tarfile
from zipfile import ZipFile
import requests
import webbrowser


class DetectManager:

    __BROWSER_LIST = ['google-chrome', 'chrome', 'chromium',
                      'chromium-browser', 'mozilla', 'firefox']
    __PARENT_DIR = dirname(dirname(abspath(__file__)))

    def detectBrowser(self):
        """Detect able to browser in system.

        Returns:
            [str]: [description]
        """
        for browser in self.__BROWSER_LIST:
            try:
                defaultBrowser = webbrowser.get(browser).name
                print(defaultBrowser)
                self.__downloadDriver(defaultBrowser)
            except Exception as e:
                print(e)

    def __downloadDriver(self,defaultBrowser):
        if defaultBrowser == 'google-chrome' or defaultBrowser == 'chrome' \
                or defaultBrowser == 'chromium' or defaultBrowser == 'chromium-browser':
            self.__downloadChromeDriver()
        elif defaultBrowser == 'mozilla' or defaultBrowser == 'firefox':
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
        return requests.get("https://chromedriver.storage.googleapis.com/LATEST_RELEASE").content.decode("UTF-8")

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

    
    def __download(self,url):
        fileName = basename(url)
        baseName, file_extension = os.path.splitext(fileName)
        with open(fileName, 'wb') as f:
            print('[*] Downloading test file of size 100 MB...')
            response = requests.get(url2, stream=True)
            total = response.headers.get('content-length')

            if total is None:
                f.write(response.content)
            else:
                downloaded = 0
                total = int(total)
                for data in response.iter_content(chunk_size=max(int(total/1000), 1024*1024)):
                    downloaded += len(data)
                    f.write(data)
                    done = int(50*downloaded/total)
                    sys.stdout.write('\r[{}{}]'.format('█' * done, '.' * (50-done)))
                    sys.stdout.flush()
        sys.stdout.write('\n')
        print('[*] Done!')

        if file_extension == '.tar' or file_extension == '.gz':
            self.__untar(fileName)
        elif file_extension == '.zip':
            self.__unzip(fileName)

    def __untar(self,file):
        if file.endswith("tar.gz"):
            tar = tarfile.open(file, "r:gz")
            tar.extractall(path=self.__PARENT_DIR+"/drivers/")
            tar.close()
        elif file.endswith("tar"):
            tar = tarfile.open(file, "r:")
            tar.extractall(path=self.__PARENT_DIR+"/drivers/")
            tar.close()
        os.remove(file)


    def __unzip(self,file):
        zf = ZipFile(file)
        zf.extractall(path=self.__PARENT_DIR+"/drivers/")
        zf.close()
        os.remove(file)
    

if __name__ == "__main__":
    detect = DetectManager()
    detect.detectBrowser()
