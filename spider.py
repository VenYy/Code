import json
from lxml import html
import random
import requests
from requests import RequestException
import time
from dbManager import Manager

# URL = "https://lab.isaaclin.cn/nCoV/api/area"
URL = "https://ncov.dxy.cn/ncovh5/view/pneumonia"
USER_AGENT_LIST = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 '
    'Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:73.0) Gecko/20100101 Firefox/73.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 '
    'Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 '
    'Safari/537.36 Edge/16.16299',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0'
]
db = Manager()


class Spider(object):

    def __init__(self):
        # self.db = Manager()
        # requests.session() 跨请求时保持某些参数
        self.session = requests.session()
        self.url = URL

    def crawl(self):
        self.session.headers.update({
            "user-agent": random.choice(USER_AGENT_LIST)
        })
        try:
            req = self.session.get(url=self.url)
            print(req.status_code)
            element = req.content.decode("utf-8")
        except RequestException as e:
            print(f"Connection Failed, {e}")

        data = html.etree.HTML(element)
        return data

    '''
    解析丁香园*https://ncov.dxy.cn/ncovh5/view/pneumonia*提供的当天国内国内数据
    解析数据并存入mysql数据库 infos.area_info 中
    '''
def parse_dxy(data):
    _ = data.xpath("//script[@id='getAreaStat']/text()")[0][27: -11]
    areaInfo = json.loads(_)
    # print(areaInfo)
    for i in range(len(areaInfo)):
        provinceName = areaInfo[i]["provinceShortName"]  # 省份名称
        # print(provinceName)
        currentConfirmedCount = areaInfo[i]["currentConfirmedCount"]  # 现存确诊人数
        confirmedCount = areaInfo[i]["confirmedCount"]  # 现存确诊人数
        suspectedCount = areaInfo[i]["suspectedCount"]  # 疑似感染人数
        curedCount = areaInfo[i]["curedCount"]  # 治愈人数
        deadCount = areaInfo[i]["deadCount"]  # 死亡人数
        statisticsData = areaInfo[i]["statisticsData"]  # 历史数据
        highDangerCount = areaInfo[i]["highDangerCount"]  # 高风险地区数
        midDangerCount = areaInfo[i]["midDangerCount"]  # 中风险地区数
        dangerAreas = areaInfo[i]["dangerAreas"]  # 风险地区列表
        # if data[i]["cities"][0]:
        #     commentName = data[i]["cities"][0]["cityName"]
        #     comment = data[i]["cities"][0]["currentConfirmedCount"]
        db.insert2areaInfo(provinceName, currentConfirmedCount, confirmedCount, suspectedCount, curedCount,
                           deadCount, highDangerCount, midDangerCount)


# 解析自*https://lab.isaaclin.cn/nCoV/*提供的api
def parse_data(self, data):
    # dict = {}
    for i in range(len(data)):
        countryName = data[i]["countryName"]  # 国家名称
        provinceShortName = data[i]["provinceShortName"]  # 省份简称
        currentConfirmedCount = data[i]["currentConfirmedCount"]  # 现存确诊人数
        suspectedCount = data[i]["suspectedCount"]  # 疑似确诊人数
        curedCount = data[i]["curedCount"]  # 治愈人数
        deadCount = data[i]["curedCount"]  # 死亡人数




        # dict["countryName"] = countryName
        # dict["provinceShortName"] = provinceShortName
        # dict["currentConfirmedCount"] = currentConfirmedCount
        # dict["suspectedCount"] = suspectedCount
        # dict["curedCount"] = curedCount
        # dict["deadCount"] = deadCount
        #
        # print(dict)
        # 全球城市数据存入数据库
        db.insert2province(countryName, provinceShortName, currentConfirmedCount, suspectedCount, curedCount,
                           deadCount)


if __name__ == '__main__':
    spider = Spider()
    while True:
        data = spider.crawl()
        parse_dxy(data)
        time.sleep(600)  # 每十分钟重新获取一次数据
