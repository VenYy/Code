import time

from flask import Flask, render_template, jsonify
from dbManager import Manager
import historyData

app = Flask(__name__)
app.config.from_object(__name__)
db = Manager()


@app.route("/")
def index():

    return render_template("index.html")


# 功能：地图显示实时数据
# 每日疫情信息，每次运行执行一边爬虫程序更新数据
'''
元组类型
    daily_info[0]: ('台湾', 11648, 13241, 431, 1133, 460, 0, 0)
    daily_info[0][0]: 台湾
'''
@app.route("/api/showMap", methods=["get", "post"])
def showMap():
    daily_info = db.get_data()
    # print(daily_info)
    currentConfirmed = []
    sumConfirmed = []

    for item in daily_info:
        currentConfirmed.append({"name": item[1], "value": item[3]})
        sumConfirmed.append({"name": item[1], "value": item[4]})
    return jsonify({"data": currentConfirmed}, {"data": sumConfirmed})


# 功能：数字屏幕
@app.route("/api/screen_info", methods=["get", "post"])
def screen_info():
    data = db.get_info()
    # print(data)
    # (Decimal('12370'), Decimal('116853'), Decimal('1868'), Decimal('5324'))
    return jsonify({"nowConfirmed": int(data[0]), "confirmed": int(data[1]), "suspected": int(data[2]), "dead": int(data[3])})

# 功能：时间显示
@app.route("/api/showTime", methods=["get", "post"])
def show_time():
    time_str = time.strftime("%Y{}%m{}%d{} %X").format("年", "月", "日")
    return time_str

# 全国新增确诊%全国新增死亡
@app.route("/api/leftTop", methods=["get", "post"])
def left_top():
    data, dateIdList = db.leftData()
    # print(data)
    confirmedIncrList = []
    curedIncrList = []
    deadIncrList = []
    for i in data:
        confirmedIncr = i[2]
        curedIncr = i[8]
        deadIncr = i[6]
        confirmedIncrList.append(confirmedIncr)
        deadIncrList.append(deadIncr)
        curedIncrList.append(curedIncr)
    return jsonify({"dateId": dateIdList[::-1], "confirmedIncr": confirmedIncrList[::-1], "deadIncr": deadIncrList[::-1], "curedIncr": curedIncrList[::-1]})

# 全国累计确诊&全国累计治愈
@app.route("/api/leftBottom", methods=["get", "post"])
def left_bottom():
    data, dateIdList = db.leftData()
    confirmedCountList = []
    curedCountList = []
    deadCountList =[]
    for i in data:
        confirmedCount = i[1]
        curedCount = i[7]
        deadCount = i[5]
        confirmedCountList.append(confirmedCount)
        curedCountList.append(curedCount)
        deadCountList.append(deadCount)

    return jsonify({"dateId": dateIdList[::-1], "confirmedCount": confirmedCountList[::-1], "curedCount": curedCountList[::-1], "deadCount": deadCountList[::-1]})


@app.route("/api/rightTop", methods=["get", "post"])
def right_top():
    data = db.rightTop_data()
    rightTopData = []
    for item in data:
        rightTopData.append({"name": item[0], "value": item[1]})
    # print(rightTopData)
    return jsonify({"data": rightTopData})

@app.route("/api/rightCenter", methods=["get", "post"])
def right_center():
    data = db.rightCenter_data()
    # print(data)
    rightCenterData = []
    for item in data:
        rightCenterData.append({"countryName": item[0], "currentConfirmedCount": item[1], "confirmedCount": item[2], "curedCount": item[3], "deadCount": item[4]})
    return jsonify({"data": rightCenterData})

if __name__ == '__main__':
    # spider = Spider()
    # data = spider.spider()
    # spider.parse_data(data)
    app.run(debug=True)

