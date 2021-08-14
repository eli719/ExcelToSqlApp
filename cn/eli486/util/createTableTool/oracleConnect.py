from cx_Oracle import DatabaseError
from cx_Oracle import connect
import logging
from tkinter.messagebox import showerror
import time

import MyThread


def count_time():
    time_start = time.time()
    time.sleep(1)
    time_end = time.time()  # 结束计时
    time_c = time_end - time_start  # 运行所花时间
    # print('time cost', time_c, 's')
    return False


def limt_connect(oracle_address):
    global con
    try:
        con = connect(oracle_address)
        return True, con
    except DatabaseError as e:
        logging.info("数据库连接异常：%s",e)
        return False


#
def test_connect(oracle_address):
    # 创建线程
    thread = MyThread(limt_connect, (oracle_address,))
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
        if str(e) == 'ORA-00955: 名称已由现有对象使用':
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