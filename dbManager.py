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
    def executeSql(self, sql):
        # 每个execute前加上互斥锁，防止多个线程同时执行造成的异常
        self.lock.acquire()
        self.cursor.execute(sql)
        self.lock.release()
        data = self.cursor.fetchall()
        # self.connClose()
        return data

    def submit(self, sql):
        try:
            if self.cursor.execute(sql):
                self.conn.commit()
                print("插入数据成功")
        except Exception as e:
            print("插入数据失败", e)
            self.conn.rollback()

    # 获取大屏需要展示的信息
    def get_info(self, args):
        sql = f"SELECT SUM(currentConfirmedCount), SUM(confirmedCount), SUM(suspectedCount), SUM(deadCount) FROM {args}"
        data = self.executeSql(sql)
        # print(data)
        return data[0]

    def get_data(self, args):
        sql = f"select * from {args}"
        data = self.executeSql(sql)
        return data
