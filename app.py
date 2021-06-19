from flask import Flask, render_template, jsonify
from dbManager import Manager
from spider import Spider

app = Flask(__name__)
app.config.from_object(__name__)
db = Manager()
spider = Spider()

@app.route("/")
def index():
    # 每日疫情信息，每次运行执行一边爬虫程序更新数据
    '''
    元组类型
        daily_info[0]: ('台湾', 11648, 13241, 431, 1133, 460, 0, 0)
        daily_info[0][0]: 台湾
    '''
    return render_template("index.html")

@app.route("/chinaMap")
def showMap():
    daily_info = db.get_data("area_info")
    return daily_info


@app.route('/totalData')
def total():
    daily_info = db.get_data("area_info")
    return render_template("totalData.html", data=daily_info)

@app.route("/ajax", methods=["get", "post"])
def test():
    return "1000"

@app.route("/screen_info", methods=["get", "post"])
def screen_info():
    data = db.get_info("area_info")
    # print(data[0][0])
    # (Decimal('12370'), Decimal('116853'), Decimal('1868'), Decimal('5324'))
    return jsonify({"nowConfirmed": int(data[0]), "confirmed": int(data[1]), "suspected": int(data[2]), "dead": int(data[3])})


if __name__ == '__main__':
    # spider = Spider()
    # data = spider.spider()
    # spider.parse_data(data)
    app.run(debug=True)

# aaa

