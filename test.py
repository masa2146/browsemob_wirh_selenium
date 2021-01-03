import os
from os.path import dirname, abspath
from os.path import basename
from os import path
import re
import tarfile
from zipfile import ZipFile
import requests
import sys


__PARENT_DIR = dirname(abspath(__file__))

def getFileName(r):
    print(r.headers)
    if 'content-disposition' in r.headers:
        d = r.headers['content-disposition']
        fname = re.findall("filename=(.+)", d)
        if len(fname) != 0:
            return fname[0]
    else:
        return basename(r.url)


def untar(file):
    if file.endswith("tar.gz"):
        tar = tarfile.open(file, "r:gz")
        tar.extractall(path=__PARENT_DIR+"/drivers/")
        tar.close()
    elif file.endswith("tar"):
        tar = tarfile.open(file, "r:")
        tar.extractall(path=__PARENT_DIR+"/drivers/")
        tar.close()
    os.remove(file)


def unzip(file):
    zf = ZipFile(file)
    zf.extractall(path=__PARENT_DIR+"/drivers/")
    zf.close()
    os.remove(file)


def download():
    url = "https://github.com/mozilla/geckodriver/releases/download/v0.28.0/geckodriver-v0.28.0-linux32.tar.gz"
    url2 = "https://chromedriver.storage.googleapis.com/87.0.4280.88/chromedriver_linux64.zip"
    # r = requests.get(url2, allow_redirects=True)
    # fileName = __PARENT_DIR+"/drivers/"+getFileName(r)
    # open(fileName, 'wb').write(r.content)
    fileName = basename(url2)
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


    # fileName = __PARENT_DIR+"/drivers/chromedriver_linux64.zip"

    if file_extension == '.tar' or file_extension == '.gz':
        untar(fileName)
    elif file_extension == '.zip':
        unzip(fileName)


download()
