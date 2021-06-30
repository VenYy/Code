import threading
import pymysql

DB_INFO = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "root",
    "charset": "utf8",
    "database": "infos"
}


class Manager(object):
    # 连接数据库
    def __init__(self):
        self.conn = pymysql.connect(host=DB_INFO["host"],
                                    user=DB_INFO["user"],
                                    password=DB_INFO["password"],
                                    port=DB_INFO["port"],
                                    charset=DB_INFO["charset"],
                                    database=DB_INFO["database"]
                                    )

        self.cursor = self.conn.cursor()
        self.lock = threading.Lock()

    # 释放资源
    def connClose(self):
        self.cursor.close()
        self.conn.close()

    # 执行sql
    def query(self, sql):
        # 每个execute前加上互斥锁，防止多个线程同时执行造成的异常
        self.lock.acquire()
        self.cursor.execute(sql)
        self.lock.release()
        data = self.cursor.fetchall()
        # self.connClose()
        return data

    def insertData(self, sql):
        try:
            if self.cursor.execute(sql):
                self.conn.commit()
                print("插入数据成功")
        except Exception as e:
            print("插入数据失败", e)
            self.conn.rollback()
        # self.connClose()

    # 获取大屏需要展示的信息
    def get_info(self):
        sql = "SELECT SUM(currentConfirmedCount), SUM(confirmedCount), SUM(suspectedCount), SUM(deadCount) FROM area_info where updateTime=(select updateTime from area_info order by updateTime desc limit 1)"
        data = self.query(sql)
        # print(data)
        return data[0]

    # 展示地图需要的数据，取时间戳最新的一组数据
    def get_data(self):
        sql = "SELECT * FROM area_info WHERE updateTime =( SELECT updateTime FROM area_info ORDER BY updateTime DESC LIMIT 1 );"
        data = self.query(sql)
        return data

    def leftData(self):
        sql = "select * from history_data order by dateId desc"
        data = self.query(sql)
        dateIdList = []
        for i in data:
            dateId = str(i[0])
            year, month, day = dateId[:4], dateId[4:6], dateId[6:8]
            time_str = f"{year}-{month}-{day}"
            dateIdList.append(time_str)
        return data, dateIdList

    def rightTop_data(self):
        sql = "select citiesName, citiesData from cities_info where(provinceName='广东') order by updateTime desc, citiesData desc limit 8"
        data = self.query(sql)
        return data

    def rightCenter_data(self):
        sql = "select countryName, currentConfirmedCount, confirmedCount, curedCount, deadCount from country_info order by updateTime desc, confirmedCount desc limit 10"
        data = self.query(sql)
        return data

    def rightBottom_data(self):
        sql = "select updateTime, totalVaccineTrend from vaccinetrend_data  where(countryName='中国') order by updateTime asc"
        data = self.query(sql)
        return data