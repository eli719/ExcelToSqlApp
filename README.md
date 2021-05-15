# ExcelToSqlApp
## Excel模板创建Oracle表

![app_view](/resources/app_view.png)

### 一、创建Excel模板

![Excel模板](/resources/excel_template.png)

### 二、解析Excel模板

- 表名必填项，表注释不填则默认为"请输入表注释"
- 模板文件生成路径不选则默认在当前用户桌面,目前只支持Windows桌面
- 数据库连接地址填写的是Oracle连接地址，输入格式为(用户名/密码@IP:端口号/服务名)，点击Test按钮尝试建立连接
- 点击解析模板，会根据模板Excel，日志文本框中将打印出流程和建表SQL

### 三、数据库建表

在与数据库连接成功后，可以将解析模板后的sql直接在oracle数据库执行，执行成功会弹出提示框，失败后弹出oracle相关错误信息。

### 关于打包成exe太大

用的是pyinstaller,因为开发环境用的是Acconda，打包时引入了很多不需要的三方库，导致生成的程序包太大，有900多MB，所以查了一下改用pipenv，只引入需要的库，结果最后变成了80MB.

前后对比图:![compare](/resources/compare.png)

参考：

[Python 打包成 exe，太大了该怎么解决？](https://www.zhihu.com/question/281858271?sort=created)

[pyinstaller failed to execute script](https://blog.csdn.net/A807296772/article/details/82769835)

