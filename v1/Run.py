import requests
from lxml import etree
import json
from os import path, mkdir, system
from time import sleep

URL = 'https://www.caranddriver.com/photos/g35491760/2021-porsche-911-turbo-drive-gallery/'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/83.0.4103.116 Safari/537.36',
}

SAVE_PATH = '.\\img\\'
download_url = []
download_name = []

response = requests.get(url=URL, headers=HEADERS)
response.encoding = 'utf-8'

# XPath
e = etree.HTML(response.text)
json_data = e.xpath('//*[@id="data-layer"]/text()')[0]
title = str(e.xpath('//title/text()')[0]).strip()
conv_json = json.loads(json_data)

# 目录创建
if not path.exists(SAVE_PATH):
    mkdir(SAVE_PATH)
if not path.exists(SAVE_PATH + title):
    mkdir(SAVE_PATH + title)
else:
    # system('chcp 65001')  # 如果终端不能正常输出或者是输出有问题，再把这个打开。否则请保持默认。
    system('tree .\img')
    if input('已存在，继续？(y)').lower() != 'y':
        print('\t结束')
        exit(0)

# 终端日志输出
print(title + '\n' + json_data + '\n')
print(str(len(conv_json['content']['images']['gallery']) / 2) + ' 个项目')

for image in conv_json['content']['images']['gallery']:
    download_url.append(str(image['url']))
    if 'hips.hearstapps.com' in str(image['url']):
        download_name.append(
            str(image['url']).replace('https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/', '')
        )
    # elif 'www.caranddriver.com' in str(image['url']):
    #     download_name.append(str(image['url']).replace('https://www.caranddriver.com/photos/g25683539/', ''))

download_url = list(set(download_url))
download_name = list(set(download_name))

# 图片保存
for name, dld_url in zip(download_name, download_url):
    sleep(3)
    with open(SAVE_PATH + title + '\\' + name, 'wb') as image_save:
        print('DOWNLOAD >> ' + name)
        resp = requests.get(url=dld_url, headers=HEADERS)
        image_save.write(resp.content)
        image_save.flush()
        image_save.close()
    print(name + ' √\n')
print('\n完成')

# 2020年8月10日 - 创建
# 2021年3月6日 - 修改
