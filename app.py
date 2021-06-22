import time

from flask import Flask, render_template, jsonify
from dbManager import Manager

app = Flask(__name__)
app.config.from_object(__name__)
db = Manager()


@app.route("/")
def index():

    return render_template("index.html")

# 实时数据
# 每日疫情信息，每次运行执行一边爬虫程序更新数据
'''
元组类型
    daily_info[0]: ('台湾', 11648, 13241, 431, 1133, 460, 0, 0)
    daily_info[0][0]: 台湾
'''
@app.route("/showMap", methods=["get", "post"])
def showMap():
    daily_info = db.get_data("area_info")
    # print(daily_info[0])
    result = []
    for item in daily_info:
        result.append({"name": item[0], "value": item[1]})
    return jsonify({"data": result})



@app.route("/screen_info", methods=["get", "post"])
def screen_info():
    data = db.get_info("area_info")
    # print(data[0][0])
    # (Decimal('12370'), Decimal('116853'), Decimal('1868'), Decimal('5324'))
    return jsonify({"nowConfirmed": int(data[0]), "confirmed": int(data[1]), "suspected": int(data[2]), "dead": int(data[3])})

@app.route("/showTime")
def show_time():
    time_str = time.strftime("{}%Y{}%m{}%d{} %X")
    return time_str.format("数据更新时间：", "年", "月", "日")


if __name__ == '__main__':
    # spider = Spider()
    # data = spider.spider()
    # spider.parse_data(data)
    app.run(debug=True)

