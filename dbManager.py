import traceback
import threading
import pymysql
from pymysql import cursors

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
    def executeSql(self, sql):
        # 每个execute前加上互斥锁
        self.lock.acquire()
        self.cursor.execute(sql)
        self.lock.release()
        data = self.cursor.fetchall()
        # self.connClose()
        return data

    # 插入实时数据
    def insert2areaInfo(self, provinceName, currentConfirmedCount, confirmedCount, suspectedCount, curedCount,
                        deadCount, highDangerCount, midDangerCount):
        sql = 'replace into area_info values("%s", "%d", "%d", "%d", "%d", "%d", "%d", "%d")' % (
            provinceName, currentConfirmedCount, confirmedCount, suspectedCount, curedCount, deadCount, highDangerCount,
            midDangerCount)
        try:
            if self.cursor.execute(sql):
                self.conn.commit()
                print("插入数据成功")
        except:
            print("插入数据失败")
            self.conn.rollback()

    # 插入历史总数据
    def insert2province(self, countryName, provinceShortName, currentConfirmedCount, suspectedCount, curedCount,
                        deadCount):
        sql = 'replace into province_info values ("%s", "%s", "%d", "%d", "%d", "%d")' % (
            countryName, provinceShortName, int(currentConfirmedCount), int(suspectedCount), int(curedCount),
            int(deadCount))
        try:
            if self.cursor.execute(sql):
                self.conn.commit()
                print("插入数据成功")
        except:
            print("插入数据失败")
            self.conn.rollback()

    # 获取大屏需要展示的信息
    def get_info(self, args):
        sql = f"SELECT SUM(currentConfirmedCount), SUM(confirmedCount), SUM(suspectedCount), SUM(deadCount) FROM {args}"
        data = self.executeSql(sql)
        return data[0]

    def get_data(self, args):
        sql = f"select * from {args}"
        data = self.executeSql(sql)
        return data

