from application import urls
import re
import pymysql
import urllib.parse
import json

def route(path):

    def function_out(func):
        # app_file = app.file_path
        # re.match("path", app_file)
        urls.route_dict[path] = func

        def function_in():
            content = func()
            return content

        return function_in

    return function_out


@route(r"/index.html")
def index(file_path):
    """主界面"""
    with open("template/index.html", "r") as file:
        content = file.read()

        conn = pymysql.connect(host="localhost", port=3306, user="root", password="mysql", database="porject_db", charset="utf8")

        cs = conn.cursor()

        # sql = "insert into focus(id) values (6);"
        # cs.execute(sql)

        sql = "select * from info;"

        cs.execute(sql)

        # content_data = str(cs.fetchall())
        content_data = ""

        for i in cs.fetchall():
            # print(i)

            str ="""
            <tr>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td><input type="button" value="添加" id="toAdd" name="toAdd" systemidvaule="%s"></td>
            </tr>

            """ % (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[1])
            content_data += str

        conn.commit()

        cs.close()

        conn.close()

        content = re.sub("{%content%}", content_data, content)

    return content


@route(r"/add/(\d*)\.html")

def add(file_path):
    """添加关注"""
    # print(file_path)
    # stock_code = 0

    ret = re.match(r"/add/(\d*)\.html", file_path)
    if ret:
        stock_code = ret.group(1)
        # print(stock_code)
        db = pymysql.connect(host='localhost', port=3306, user='root', password='mysql', database='porject_db', charset='utf8')

        cursor = db.cursor()

        # sql = "select id from focus;"
        #
        # cursor.execute(sql)
        #
        # cur = cursor.fetchall()
        # print(stock_code+"------>")
        sql = "select * from info aa inner join focus bb on aa.id=bb.id where aa.code=%s;" % (stock_code)
        cursor.execute(sql)
        cur = cursor.fetchone()
        if cur:
            # print(stock_code)

            cursor.close()
            db.close()
            return "已经关注过了，请不要重复关注"


        else:
            sql = """insert into focus(id) select id from info where code="%s";""" % (stock_code)
            cursor.execute(sql)
            db.commit()
            cursor.close()
            db.close()
            return "关注成功"


@route(r"/center.html")
def center(file_path):
    """个人中心"""
    with open("template/center.html") as file:
        content = file.read()

        return content


@route("/center_data.html")
def center_data(file_path):
    """运用ajax"""
    conn = pymysql.connect(host="localhost", port=3306, user="root", password="mysql", database="porject_db", charset="utf8")

    cs = conn.cursor()

    sql = "select aa.code,aa.short,aa.chg,aa.turnover,aa.price,aa.highs,bb.note_info from info aa inner join focus bb on aa.id=bb.id;"

    cs.execute(sql)

    contenr_data = cs.fetchall()

    # ('002019', '亿帆医药', '1.19%', '2.81%', Decimal('17.05'), Decimal('16.85')
    contenr_data_list = [{"code": row[0],
                          "short": row[1],
                          "chg": row[2],
                          "turnover": row[3],
                          "price": str(row[4]),  # 因为这里不是字符串 是Decimal('17.05')
                          "highs": str(row[5]),  # 同理不是字符串
                          "note_info": row[6]
                          } for row in contenr_data]
    # 将列表同过json模块转化成浏览器识别的数组
    json_str = json.dumps(contenr_data_list)

    cs.close()
    conn.close()

    return json_str
    # return str(content_data)



@route(r"/del/(\d*)\.html")
def dele(file_path):
    """删除"""
    # print(file_path)
    # stock_code = 0

    ret = re.match(r"/del/(\d*)\.html", file_path)
    if ret:
        stock_code = ret.group(1)
        print(stock_code)
        db = pymysql.connect(host='localhost', port=3306, user='root', password='mysql', database='porject_db', charset='utf8')

        cursor = db.cursor()

        # sql = "select id from focus;"
        #
        # cursor.execute(sql)
        #
        # cur = cursor.fetchall()
        # print(stock_code+"------>")
        sql = "select * from focus where id=(select aa.id from info aa where aa.code=%s);" % (stock_code)
        cursor.execute(sql)
        cur = cursor.fetchone()
        print(cur)
        if cur:
            sql = "delete from focus where id=(select aa.id from info aa where aa.code='%s');" % (stock_code)
            cursor.execute(sql)
            db.commit()
            cursor.close()
            db.close()
            return "删除成功"

        else:
            cursor.close()
            db.close()
            return "数据不存在！"


@route(r"/update/(\d*)\.html")
def update(file_path):
    """更新"""
    with open("template/update.html") as file:
        content = file.read()

        ret = re.match(r"/update/(\d*)\.html", file_path)
        if ret:
            update_code = ret.group(1)

            content = re.sub("{%code%}", update_code, content)

    return content

# "/update/{%code%}/" + item + ".html"

@route(r"/update/(\d*)/(.*)\.html")
def update_note_info(file_path):
    """数据更新"""

    ret = re.match(r"/update/(\d*)/(.*)\.html", file_path)

    if ret:
        stock_code = ret.group(1)
        stock_note_info = ret.group(2)
        # print(type(stock_note_info))
        aa = urllib.parse.unquote(stock_note_info)


        conn = pymysql.connect(host="localhost", port=3306, user="root", password="mysql", database="porject_db",
                               charset="utf8")

        cs = conn.cursor()

        sql = """update focus set note_info= "%s" where id=(select aa.id from info aa where aa.code=%s);""" % (aa, stock_code)

        cs.execute(sql)

        conn.commit()

        cs.close()

        conn.close()

    return "修改成功"



