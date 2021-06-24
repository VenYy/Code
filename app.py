import time

from flask import Flask, render_template, jsonify
from dbManager import Manager

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
@app.route("/showMap", methods=["get", "post"])
def showMap():
    daily_info = db.get_data("area_info")
    # print(daily_info)
    result = []
    for item in daily_info:
        result.append({"name": item[0], "value": item[1]})
    return jsonify({"data": result})


# 功能：数字屏幕
@app.route("/screen_info", methods=["get", "post"])
def screen_info():
    data = db.get_info("area_info")
    # print(data[0][0])
    # (Decimal('12370'), Decimal('116853'), Decimal('1868'), Decimal('5324'))
    return jsonify({"nowConfirmed": int(data[0]), "confirmed": int(data[1]), "suspected": int(data[2]), "dead": int(data[3])})

# 功能：时间显示
@app.route("/showTime")
def show_time():
    time_str = time.strftime("{}%Y{}%m{}%d{} %X")
    return time_str.format("数据更新时间：", "年", "月", "日")

# 功能：left_top显示当前确诊人数最多的前几个城市
@app.route("/leftTop")
def left_top():
    datas = db.get_left_top()
    data = []
    # print(data)
    # (('广东', '广州', 134), ('上海', '境外输入k ', 55), ('福建', '境外输入人员', 46), ('浙江', '境外输入', 45), ('广东', '深圳', 44), ('四川', '成都', 42),
    # ('云南', '境外输入', 41), ('北京', '境外输入', 28), ('广东', '佛山', 19), ('江苏', '境外输入', 14))
    for item in datas:
        data.append({"provinceName": item[0], "citiesName": item[1], "citiesData": item[2]})
    return jsonify({"data": data})



if __name__ == '__main__':
    # spider = Spider()
    # data = spider.spider()
    # spider.parse_data(data)
    app.run(debug=True)

