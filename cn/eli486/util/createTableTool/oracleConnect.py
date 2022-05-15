from cx_Oracle import DatabaseError
from cx_Oracle import connect
import logging
from tkinter.messagebox import showerror
import time
import pymysql as mysql
from pymysql import OperationalError

from MyThread import MyThread


def count_time():
    time_start = time.time()
    time.sleep(1)
    time_end = time.time()  # 结束计时
    time_c = time_end - time_start  # 运行所花时间
    # print('time cost', time_c, 's')
    return False


def limt_connect(address, dbType):
    global con
    if dbType == 1:
        try:
            con = connect(address)
            return True, con
        except DatabaseError as e:
            logging.info("数据库连接异常：%s", e)
            return False
    else:
        # user/pwd@ip:port/sid
        first = address[0:address.index('@')].split("/")
        second = address[address.index('@') + 1:].split("/")
        host_port = second[0].split(":")
        # db = mysql.connect(host="192.168.227.129", user="root", passwd="123456", port=3306, db="", charset="utf8")
        try:
            con = mysql.connect(host=host_port[0], user=first[0], passwd=first[1], port=int(host_port[1]), db=second[1],
                                charset="utf8")
            return True, con
        except OperationalError as e:
            logging.info("数据库连接异常：%s", e)
            return False


def test_connect(oracle_address, type):
    # 创建线程
    thread = MyThread(limt_connect, (oracle_address, type))
    # 启动线程
    thread.start()
    count_time()
    # print(thread.get_result())
    if thread.get_result() is None:
        showerror('错误', "连接超时")
        return
    return thread.get_result()


def create_table(conn, sqlList):
    cursor = conn.cursor()
    try:
        for sql in sqlList[0]:
            cursor.execute(sql)
    except DatabaseError as e:
        logging.error(str(e))
        if str(e) == 'ORA-00955: 名称已由现有对象使用':
            showerror('错误', "该表名已被创建，请检查!")
            return False
        showerror('错误', e)
        logging.warning(e)
        cursor.execute(sqlList[1])
        return False
    except OperationalError as e:
        logging.error(str(e))
        if str(e).index("1050") != -1:
            showerror('错误', "该表名已被创建，请检查!")
            return False
        showerror('错误', e)
        logging.warning(e)
        cursor.execute(sqlList[1])
        return False
    finally:
        cursor.close()
        # connect.close()
    return True


def delete_table(con, sql):
    cursor = con.cursor()
    try:
        cursor.execute(sql)
    except DatabaseError as e:
        if str(e) == 'ORA-00955: 名称已由现有对象使用':
            showerror('错误', "该表名已被创建，请检查!")
            return False
        showerror('错误', e)
        logging.warning(e)
        return False
    finally:
        cursor.close()
    return True
