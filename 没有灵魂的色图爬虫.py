import os, time
import requests
from random import randint
from threading import Thread
from bs4 import BeautifulSoup


def rndSlp(start, end):
    time.sleep(randint(start, end))


class sankaku():
    def __init__(self, tag, savePath):
        threashold = 4
        print('Start search %s on SankakuComplex\nThreashold = %s' % (tag, threashold))
        for page in range(1, 1000):
            rndSlp(3, 5)
            webPage = 'https://chan.sankakucomplex.com/?tags=%s&page=%s' % (tag, page)
            resp = requests.get(webPage)
            bs = BeautifulSoup(resp.text, 'lxml')
            idList = []
            for value in bs.find_all('span', class_='thumb blacklisted'):
                value = str(value)
                score = float(value.split('Score:')[1].split(' ')[0])
                if score >= threashold:
                    id = value.split('"p')[1].split('"')[0]
                    if not os.path.exists(os.path.join(savePath, id)):
                        rndSlp(20, 30)
                        Thread(target=self.dnld, args=(id, savePath)).start()

    def dnld(self, id, savePath):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
        postLink = 'https://chan.sankakucomplex.com/post/show/%s' % id
        print(postLink)
        resp = requests.get(postLink, headers=headers)
        bs = BeautifulSoup(resp.text, 'lxml')
        value = str(bs.find('div', id='post-content'))
        if 'image-link' in value:  # image
            if 'sample' in value:
                source = 'https:' + value.split('href="')[1].split('"')[0].replace('amp;', '')
            else:
                source = 'https:' + value.split('src="')[1].split('"')[0].replace('amp;', '')
            format = source.split('.')[-1].split('?')[0]
            rndSlp(2, 3)
            pic = requests.get(source, headers=headers)
            if pic.status_code == 200:
                with open(r'%s\%s.%s' % (savePath, id, format), 'wb') as fp:
                    fp.write(pic.content)
                    fp.close()
        elif 'vedio' in value:  # 视频下载 咕咕咕
            pass


if __name__ == '__main__':
    rootPath = r'E:\没有灵魂的色图文件夹'
    if not os.path.exists(rootPath):
        os.mkdir(rootPath)
    tags = ['BDSM', 'legwear', 'gloves', 'otoko_no_ko']
    for tag in tags:
        savePath = os.path.join(rootPath, tag)
        if not os.path.exists(savePath):
            os.mkdir(savePath)
        Thread(target=sankaku, args=(tag, savePath)).start()
