import os
import re
from tkinter.filedialog import askopenfilename, askdirectory
from tkinter import Tk
from tkinter import Label
from tkinter import StringVar
from tkinter import Button
from tkinter import Entry
from tkinter.constants import END
from tkinter.messagebox import showinfo, showerror, showwarning, askyesno, askokcancel
from tkinter import scrolledtext
from tkinter.ttk import Combobox

from parseExcel import excel_to_sql, create_template
import winreg
import logging
from oracleConnect import create_table, test_connect, delete_table

connect = ''


def get_desktop():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                         r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')

    return winreg.QueryValueEx(key, "Desktop")[0]


def get_address():
    if os.path.exists('address.txt'):
        with open('address.txt', mode='r') as f1:
            b = f1.read()
        c = set(b.split('\n'))
        return list(c)
    else:
        return []


class MyGui:

    def __init__(self, init_window_name):
        self.type = 1
        self.path = StringVar()
        self.fileName = StringVar()
        self.sql = ()
        self.init_window_name = init_window_name
        # var = StringVar()
        self.c = get_address()

        logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                            level=logging.DEBUG, stream=self)
        # 设置窗口大小(最小值：像素)
        # self.init_window_name.minsize(500, 500)
        self.init_window_name.title('🤴の🗡')
        self.init_window_name.iconbitmap('击剑.ico')
        sw = self.init_window_name.winfo_screenwidth()
        sh = self.init_window_name.winfo_screenheight()
        # print(sw,sh)

        # self.init_window_name.geometry('620x600+500+100')
        self.init_window_name.geometry('%dx%d+%d+%d' % (sw / 2, 2 * sh / 3, sw / 4, sh / 6))
        # 第一行
        Label(self.init_window_name, text="表名").grid(row=1, column=0)
        self.table_name = Entry(self.init_window_name)
        self.table_name.grid(row=1, column=1, padx=10, pady=10)
        Label(self.init_window_name, text="表注释").grid(row=1, column=2)
        self.table_comment = Entry(self.init_window_name)
        self.table_comment.grid(row=1, column=3, padx=10, pady=10)
        # 第二行
        Label(self.init_window_name, text="生成路径(默认桌面):").grid(row=2, column=0)
        self.template = Entry(self.init_window_name, textvariable=self.path)
        self.template.grid(row=2, column=1, padx=10, pady=10)
        Button(self.init_window_name, text="选择路径", width=20, command=self.selectPath).grid(row=2, column=3)
        # 第三行
        Button(self.init_window_name, text="创建模板", command=self.create).grid(row=3, column=1, columnspan=2,
                                                                             ipadx=80)
        # 第四行
        Label(self.init_window_name, text="模板文件名:").grid(row=4, column=0)
        self.mode_file = Entry(self.init_window_name, textvariable=self.fileName)
        self.mode_file.grid(row=4, column=1, padx=10, pady=10)
        Button(self.init_window_name, text="选择文件", command=self.selectTemplateFile).grid(row=4, column=3, ipadx=20)
        # 第五行
        Label(self.init_window_name, text="数据库连接地址(user/pwd@ip:port/sid):").grid(row=5, column=0, ipadx=10)
        # self.oracle_address = Entry(self.init_window_name)

        self.oracle_address = Combobox(self.init_window_name, values=self.c, width=35)
        self.oracle_address.grid(row=5, column=1, pady=10)
        Button(self.init_window_name, text="OracleTest", command=self.oracle).grid(row=5, column=2)
        Button(self.init_window_name, text="MysqlTest", command=self.mysql).grid(row=5, column=3)
        # 第六行
        Button(self.init_window_name, text="解析模板", command=self.parseTemplate).grid(row=6, column=0, ipadx=80)
        Button(self.init_window_name, text="重置", command=self.clear).grid(row=6, column=1)
        Button(self.init_window_name, text="数据库建表", command=self.database_execute).grid(row=6, column=2, ipadx=10)

        Button(self.init_window_name, text="数据库删表", command=self.delete_table).grid(row=6, column=3, ipadx=14)
        # 第七行
        Label(self.init_window_name, text="日志：").grid(row=7, column=0)
        # 第八行
        self.log = scrolledtext.ScrolledText(self.init_window_name)
        self.log.grid(row=8, column=0, columnspan=4)

    def selectPath(self):
        if self.table_name.get().strip() == '':
            showinfo('提示', '请输入表名')
            return
        logging.info("选择路径")
        absolute_path = os.path.join(askdirectory(), self.table_name.get() + ".xlsx")
        self.path.set(absolute_path)

    def create(self):
        if self.table_name.get().strip() == '':
            showinfo('提示', '请输入表名!')
            return
        if self.path.get().strip() == '':
            absolute_path = os.path.join(get_desktop(), self.table_name.get() + ".xlsx")
            self.path.set(absolute_path)
        filename = self.path.get()
        create_template(filename, self.table_comment.get())
        flag = askyesno('提示', '是否打开已创建的模板文件?')
        if flag:
            os.startfile(self.path.get())

    def selectTemplateFile(self):
        self.fileName.set(askopenfilename())

    def parseTemplate(self):
        f = self.fileName.get().strip()
        if f == '':
            showinfo('提示', '请选择要解析的模板excel')
            return
        flag = os.path.exists(f)
        if flag is False:
            showinfo('提示', 'excel模板文件不存在!')
            return
        logging.info("选择文件:" + f)
        file_type = os.path.basename(f).split(".")[1]
        if file_type != 'xlsx':
            showerror('提示', '暂不支持非EXCEL格式文件解析!')
            return
        self.sql = excel_to_sql(f, self.type)
        if self.sql is None:
            showinfo('提示', '模板文件内无数据')

    def write(self, s):
        self.log.insert(END, s)
        self.log.yview_moveto(1)
        self.log.update()

    def oracle(self):
        self.type = 1
        global connect
        address = self.oracle_address.get().strip()
        if address == '':
            showinfo('提示', '请输入oracle数据库地址')
        elif re.match(r"^\w+/\w+@(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25["
                      r"0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d):\d+/\w+$",
                      address) is None:
            showinfo('提示', '请匹配oracle连接格式:user/pwd@ip:port/sid')
            return
        else:
            result = test_connect(self.oracle_address.get(), self.type)
            if result:
                connect = result[1]
                if self.c.count(address) == 0:
                    logging.info("数据库连接成功:" + address)
                    self.c.append(address)
                    self.oracle_address['values'] = self.c
                    f = open('address.txt', 'w')
                    f.write('\n'.join(self.c))
                    f.close()
                showinfo('提示', '数据库连接成功')
            else:
                showwarning('错误', '数据库连接失败')

    def mysql(self):
        self.type = 2
        global connect
        address = self.oracle_address.get().strip()
        if address == '':
            showinfo('提示', '请输入oracle数据库地址')
        elif re.match(r"^\w+/\w+@(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25["
                      r"0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d):\d+/\w+$",
                      address) is None:
            showinfo('提示', '请匹配oracle连接格式:user/pwd@ip:port/sid')
            return
        else:
            result = test_connect(self.oracle_address.get(), self.type)
            if result:
                connect = result[1]
                if self.c.count(address) == 0:
                    logging.info("数据库连接成功:" + address)
                    self.c.append(address)
                    self.oracle_address['values'] = self.c
                    f = open('address.txt', 'w')
                    f.write('\n'.join(self.c))
                    f.close()
                showinfo('提示', '数据库连接成功')
            else:
                showwarning('错误', '数据库连接失败')

    def database_execute(self):
        if connect == '':
            showinfo('提示', '请先尝试连接oracle数据库')
            return
        if self.sql is None or len(self.sql) == 0:
            showinfo('提示', '请先执行解析模板')
            return
        flag = create_table(connect, self.sql)
        if flag:
            showinfo('提示', '执行成功')
        else:
            logging.info("建表失败，建表SQL回滚")
        self.sql = ()

    def delete_table(self):
        table_name = self.table_name.get().strip()
        if table_name == '':
            table_name = os.path.basename(self.fileName.get().strip()).split('.')[0]
        self.sql = "drop table " + table_name
        if connect == '':
            showinfo('提示', '请先尝试连接oracle数据库')
            return
        flag = askokcancel('提示', '确定删除表：' + table_name)
        if flag:
            flag = delete_table(connect, self.sql)
            if flag:
                showinfo('提示', '执行成功')
            else:
                logging.info("删表失败，回滚")
            self.sql = ()

    def clear(self):
        self.table_name.delete(0, END)
        self.table_comment.delete(0, END)
        self.template.delete(0, END)
        self.mode_file.delete(0, END)
        self.oracle_address.delete(0, END)
        self.log.delete('1.0', END)


if __name__ == '__main__':
    tk = Tk()
    a = MyGui(tk)
    tk.mainloop()
