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
    def __init__(self):
        self.conn = pymysql.connect(host=DB_INFO["host"],
                                    user=DB_INFO["user"],
                                    password=DB_INFO["password"],
                                    port=DB_INFO["port"],
                                    charset=DB_INFO["charset"],
                                    database=DB_INFO["database"]
                                    )

        self.cursor = self.conn.cursor()

    def insert2province(self, countryName, provinceShortName, currentConfirmedCount, suspectedCount, curedCount, deadCount):
        sql = 'replace into province_info values ("%s", "%s", "%d", "%d", "%d", "%d")' % (countryName, provinceShortName, int(currentConfirmedCount), int(suspectedCount), int(curedCount), int(deadCount))
        try:
            if self.cursor.execute(sql):
                self.conn.commit()
                print("插入数据成功")
        except:
            print("插入数据失败")
            self.conn.rollback()

    def insert2areaInfo(self, provinceName, currentConfirmedCount, confirmedCount, suspectedCount, curedCount, deadCount, highDangerCount, midDangerCount):
        sql = 'replace into area_info values("%s", "%d", "%d", "%d", "%d", "%d", "%d", "%d")' % (provinceName, currentConfirmedCount, confirmedCount, suspectedCount, curedCount, deadCount, highDangerCount, midDangerCount)
        try:
            if self.cursor.execute(sql):
                self.conn.commit()
                print("插入数据成功")
        except:
            print("插入数据失败")
            self.conn.rollback()

    def get_data(self, args):
        sql = f"select * from {args}"
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return data

    # 获取大屏info数据
    def get_info(self, args):
        sql = f"SELECT SUM(currentConfirmedCount), SUM(confirmedCount), SUM(suspectedCount), SUM(deadCount) FROM {args}"
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return data[0]