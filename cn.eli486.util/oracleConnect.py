from cx_Oracle import DatabaseError
from cx_Oracle import connect
import logging
from tkinter.messagebox import showerror


# clpnb/clpnb@192.168.227.130:1521/orcl
def test_connect(oracle_address):
    global con
    try:
        con = connect(oracle_address)
        return True, con
    except DatabaseError:
        # print("连接异常")
        return False


def create_table(connect, sqlList):
    cursor = connect.cursor()
    try:
        for sql in sqlList[0]:
            cursor.execute(sql)
    except DatabaseError as e:
        # print(str(e))
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

# if __name__ == '__main__':
#     c = test_connect("clpnb/clpnb@192.168.227.130:1521/orcl")
#     c[1].cursor().execute('''DECLARE
# 	sqlt VARCHAR(200);
# begin
# 	sqlt:='CREATE TABLE a(PK_ID VARCHAR2(90),Entnm VARCHAR2(90))';
# 	execute immediate sqlt;
#
# 	sqlt:='comment on table a is '||'asd'||'';
# 	execute immediate sqlt;
# EXCEPTION
# WHEN OTHERS THEN
# 	sqlt:= 'DROP TABLE A';
# 	execute immediate sqlt;
# end;
# ''')
