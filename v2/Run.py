import requests
from time import sleep
from sys import platform
from lxml import etree
from rich import print
from os.path import exists
from os import mkdir
import json


class CarAndDriverSpider:
    url = ''
    img_list1 = []
    img_list2 = []

    def __init__(self):
        self.url = 'https://www.caranddriver.com/photos/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
        }
        self.cdn = ['https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/', ]
        self.count = 1

    @staticmethod
    def mk_dir(img_dir):
        if not exists(img_dir):
            mkdir(img_dir)

    def img_spider(self, url):
        if self.url in url:
            str1 = url.replace(self.url, '')
            cut = str1.index('/')
            print(self.url + '[bold green]' + str1[:cut] + '[/bold green]' + str1[9:] + ' 提示：可直接使用绿色部分启动程序')
            CarAndDriverSpider.url = url + '?slide=1'
        else:
            CarAndDriverSpider.url = self.url + url + '?slide=1'
            print(CarAndDriverSpider.url)

        response = requests.get(url=CarAndDriverSpider.url, headers=self.headers)
        response.encoding = 'utf-8'
        e = etree.HTML(response.text)
        json_data = e.xpath('//script[@id="data-layer"]/text()')[0]
        json_data = json.loads(json_data)
        title = json_data['content']['title']
        self.mk_dir(img_dir=title)
        CarAndDriverSpider.img_list1 = json_data['content']['images']['gallery']
        for i in CarAndDriverSpider.img_list1:
            CarAndDriverSpider.img_list2.append(i['url'])
        CarAndDriverSpider.img_list2 = list(set(CarAndDriverSpider.img_list2))

        print('\n[bold red]----------Json Debug----------[/bold red]')
        print(CarAndDriverSpider.img_list2, len(CarAndDriverSpider.img_list2))
        print('[bold red]----------End Json Debug----------[/bold red]')

        for i in CarAndDriverSpider.img_list2:
            filename = ''
            if 'https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/' in i:
                filename = i.replace('https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/', '')
            sleep(1)
            with open('.\\' + title + '\\' + filename, 'wb') as save_image:
                img_response = requests.get(url=i)
                save_image.write(img_response.content)
                print(i + '[bold green] √[/bold green] ' + str(self.count) + '/' + str(len(CarAndDriverSpider.img_list2)))
                self.count += 1
        print('[bold green]All Done.[/bold green]')

    def run(self, url):
        self.img_spider(url=url)


if __name__ == '__main__':
    try:
        assert ('win' in platform), 'only windows platform.'.title()
        CarAndDriverSpider().run(
            # 支持两种格式 自动检测：
            #               https://www.caranddriver.com/photos/g26358386/2019-ram-2500-3500-first-drive-gallery/
            #               g26358386
            url='g34133086'
            # 如果使用g编号失败，请用完整URL
        )
    except AssertionError as AE:
        print(AE)
    except KeyboardInterrupt as KI:
        print(KI)
