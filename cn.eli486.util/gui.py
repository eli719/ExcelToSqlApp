from tkinter.filedialog import *
from tkinter.messagebox import *
from tkinter import Tk
from tkinter import Label
from tkinter import StringVar
from tkinter import Button
from tkinter import Entry
from tkinter import Text
from tkinter.constants import INSERT


from parseExcel import excel_to_sql, create_template
import winreg
import logging
from oracleConnect import create_table, test_connect

connect = ''


class MyGui:

    def __init__(self, init_window_name):
        self.path = StringVar()
        self.fileName = StringVar()
        self.sql = ()
        self.init_window_name = init_window_name

    def set_init_window(self):
        logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                            level=logging.DEBUG, stream=self)

        # 设置窗口大小(最小值：像素)
        # self.init_window_name.minsize(500, 500)
        self.init_window_name.geometry('620x500+500+200')
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
        Entry(self.init_window_name, textvariable=self.fileName).grid(row=4, column=1, padx=10, pady=10)
        Button(self.init_window_name, text="选择文件", command=self.selectTemplateFile).grid(row=4, column=3, ipadx=20)
        # 第五行
        Label(self.init_window_name, text="数据库连接地址(user/pwd@ip:port/sid):").grid(row=5, column=0)
        self.oracle_address = Entry(self.init_window_name)
        self.oracle_address.grid(row=5, column=1, pady=10)
        Button(self.init_window_name, text="Test", command=self.test).grid(row=5, column=3, ipadx=32)
        # 第六行
        Button(self.init_window_name, text="解析模板", command=self.parseTemplate).grid(row=6, column=1, columnspan=2,
                                                                                    ipadx=80)
        Button(self.init_window_name, text="数据库建表", command=self.database_execute).grid(row=6, column=3, ipadx=14)
        # 第七行
        Label(self.init_window_name, text="日志：").grid(row=7, column=0)
        # 第八行
        self.log = Text(self.init_window_name)
        self.log.grid(row=8, column=0, columnspan=4)

    def get_desktop(self):
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')

        return winreg.QueryValueEx(key, "Desktop")[0]

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
            absolute_path = os.path.join(self.get_desktop(), self.table_name.get() + ".xlsx")
            # print(absolute_path)
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
        self.sql = excel_to_sql(f)

    def write(self, s):
        self.log.insert(INSERT, s)

    def test(self):
        global connect
        address = self.oracle_address.get().strip()
        if address == '':
            showinfo('提示', '请输入oracle数据库地址')
        else:
            result = test_connect(self.oracle_address.get())
            if result:
                connect = result[1]
                showinfo('提示', '数据库连接成功')
            else:
                showwarning('错误', '数据库连接失败')

    def database_execute(self):
        if connect == '':
            showinfo('提示', '请先尝试连接oracle数据库')
            return
        if len(self.sql) == 0:
            showinfo('提示', '请先执行解析模板')
            return
        flag = create_table(connect, self.sql)
        if flag:
            showinfo('提示', '执行成功')
        else:
            logging.info("建表失败，建表SQL回滚")


if __name__ == '__main__':
    tk = Tk()
    a = MyGui(tk)
    a.set_init_window()
    tk.mainloop()
