from pandas import DataFrame
from pandas import read_excel
from Field import *
import os
import logging


def create_template(fileName, table_comment):
    logging.info("========开始创建模板Excel %s=========", fileName)
    data = [["字段名", "注释", "字段类型", "是否允许为空", "约束类型", "约束名称", "索引类型", "索引名称"]]
    if table_comment == '':
        table_comment = '请输入表注释'
    DataFrame(data).to_excel(fileName, index=False, header=False, sheet_name=table_comment)
    logging.info("========创建模板Excel完成=========")


def excel_to_sql(fileName, dbType):
    logging.info("========开始解析模板Excel %s=========", fileName)
    table_name = os.path.basename(fileName).split(".")[0]
    logging.info("========表名为 %s=========", table_name)
    data = read_excel(fileName, sheet_name=None)
    table_comment = list(data.keys())[0]
    logging.info("========表注释为 %s=========", table_comment)
    content = data.get(table_comment)
    rows = []
    cv = content.values
    if len(cv) == 0:
        logging.info("=======模板文件内无数据==========")
        return
    for i in content.values:
        if str(i[0]) == 'nan':
            continue
        f = Field(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7])
        rows.append(f)
    c = []
    c2 = []
    comments = []
    primary_name = ""
    primaries = []
    constraints = []
    indexes = []
    for j in rows:
        if j.name is None:
            continue
        comments.append("comment on column " + table_name + "." + j.name + " is '" + j.comment + "'")
        if j.is_empty:
            c.append(j.name + ' ' + j.kinds)
            c2.append(j.name + ' ' + j.kinds + ' ' + "comment " + "'" + j.comment + "'")
        else:
            c.append(j.name + ' ' + j.kinds + ' ' + 'not null')
            c2.append(j.name + ' ' + j.kinds + ' ' + 'not null' + ' ' + "comment " + "'" + j.comment + "'")

        if str(j.constrainType).lower() == "primary":
            # print(j.constrainName)
            # print(type(j.constrainName))
            if str(j.constrainName) != 'nan':
                primary_name = str(j.constrainName)
            primaries.append(j.name)
        elif str(j.constrainType).lower() == "unique":
            constraints.append("alter table " + table_name + " add constraint " + str(
                j.constrainName) + " unique " + "(" + j.name + ")")
        if str(j.indexType).lower() != 'nan':
            if str(j.indexType).lower() == "unique":
                indexes.append("create unique index " + str(j.indexName) + " on " + table_name + " (" + j.name + ")")
            else:
                indexes.append("create index " + str(j.indexName) + " on " + table_name + " (" + j.name + ")")
    # print(','.join(c))
    # print(','.join(primaries))
    # print(';'.join(constraints))
    # print(';'.join(indexes))
    # print(''.join(comments))
    sql = []
    if dbType == 1:
        body = ','.join(c)
        create_table_sql = 'CREATE TABLE ' + table_name + '(' + body + ')'
        comment = "comment on table " + table_name + " is '" + table_comment + "'"
        sql = [create_table_sql, comment]
        sql.extend(comments)
    else:
        body = ','.join(c2)
        create_table_sql = 'CREATE TABLE ' + table_name + '(' + body + ')'
        sql = [create_table_sql]

    if len(primaries) > 0:
        p = ','.join(primaries)
        primary = ["alter table " + table_name + " add constraint " + primary_name + " primary key (" + p + ")"]
        sql.extend(primary)

    sql.extend(constraints)
    sql.extend(indexes)
    drop_sql = "drop table " + table_name
    # print(sql)
    # print(create_table_sql)
    # print(comment)
    # print(primary)
    logging.info("========解析完成,建表SQL为\r\n%s=========", ';\r\n'.join(sql))
    return sql, drop_sql
