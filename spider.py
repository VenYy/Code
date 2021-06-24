import json
from lxml import html
import random
import requests
from requests import RequestException
import time
from dbManager import Manager

# URL = "https://lab.isaaclin.cn/nCoV/api/area"
url = "https://ncov.dxy.cn/ncovh5/view/pneumonia"
headers = {
    "UserAgent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 '
                 'Safari/537.36'
}
db = Manager()


def change_proxy():
    useful_proxy = []
    with open("proxy_list.txt", "r") as f:
        for line in f.readlines():
            proxy = line.strip("\n")
            print(proxy)
            if requests.get(proxy).status_code == 200:
                proxy_support = {
                    "http": proxy
                }
                useful_proxy.append(proxy_support)
    return useful_proxy


# print(change_proxy())

def crawl():
    try:
        req = requests.get(url, headers=headers)
        print(req.status_code)
        page = req.content.decode("utf-8")
        data = html.etree.HTML(page)
        return data
    except RequestException as e:
        print(f"Connection Failed, {e}")


'''
解析丁香园*https://ncov.dxy.cn/ncovh5/view/pneumonia*提供的当天国内国内数据
解析数据并存入mysql数据库 infos.area_info 中
'''


def parse_dxy(data):
    _ = data.xpath("//script[@id='getAreaStat']/text()")[0][27: -11]
    areaInfo = json.loads(_)
    # print(areaInfo)
    time_str = time.strftime("%Y%m%d%H%M%S")
    # print(time_str)
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

        # 插入实时数据
        sql1 = 'replace into area_info values("%s", "%d", "%d", "%d", "%d", "%d", "%d", "%d")' % (
            provinceName, currentConfirmedCount, confirmedCount, suspectedCount, curedCount, deadCount, highDangerCount,
            midDangerCount)
        db.submit(sql1)

        citiesNameList = []
        citiesDataList = []

        # 执行插入数据库操作时，含有部分cities为空的项，以此需要将此项添加进去
        # if len(areaInfo[i]["cities"]) == 0:
        #     # print(areaInfo[i]["provinceShortName"])
        #     citiesNameList.append(areaInfo[i]["provinceShortName"])
        #     citiesDataList.append(areaInfo[i]["currentConfirmedCount"])
        if provinceName == "香港" or provinceName == "澳门" or provinceName == "台湾":
            continue
        else:
            for j in range(len(areaInfo[i]["cities"])):
                citiesName = areaInfo[i]["cities"][j]["cityName"]
                citiesData = areaInfo[i]["cities"][j]["currentConfirmedCount"]
                citiesNameList.append(citiesName)
                citiesDataList.append(citiesData)

        # 插入的时间格式 %Y%m%d%H%M%S 20210623122420，执行查询操作时需排序选取
        for n, d in zip(citiesNameList, citiesDataList):
            # print(n, d)
            sql2 = "insert into cities_info values ('%s', '%s', '%s', '%d')" % (time_str, provinceName, n, d)
            db.submit(sql2)
        # print(citiesName, citiesDict)
        # 广东
        # {'广州': 156, '深圳': 45, '佛山': 19, '珠海': 7, '东莞': 4, '湛江': 3, '中山': 2, '江门': 2, '肇庆': 1, '惠州': 0, '汕头': 0, '梅州': 0,
        #  '茂名': 0, '阳江': 0, '清远': 0, '揭阳': 0, '韶关': 0, '潮州': 0, '汕尾': 0, '河源': 0, '待明确地区': -18}


# 解析自*https://lab.isaaclin.cn/nCoV/*提供的api
def parse_data(data):
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

        sql = 'replace into province_info values ("%s", "%s", "%d", "%d", "%d", "%d")' % (
            countryName, provinceShortName, int(currentConfirmedCount), int(suspectedCount), int(curedCount),
            int(deadCount))
        db.submit(sql)


if __name__ == '__main__':
    while True:
        data = crawl()
        parse_dxy(data)
        time.sleep(600)  # 每十分钟重新获取一次数据
