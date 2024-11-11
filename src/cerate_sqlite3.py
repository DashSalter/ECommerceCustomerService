import sqlite3

#  描述数据库表结构
database_schema_string = """
CREATE TABLE product(
    id INT PRIMARY KEY NOT NULL, -- 主键，不允许为空
    product_title STR NOT NULL, -- 名称
    product_link STR NOT NULL, -- 商品详情链接
    product_price DECIMAL(10,2)  NOT NULL, --  商品价格
    product_brand STR NOT NULL -- 商品品牌
);
"""

# 创建数据库连接
conn = sqlite3.connect('product_db.db')
cursor = conn.cursor()

# 创建orders表
cursor.execute(database_schema_string)

# 插入5条明确的模拟记录
mock_data = [
    (1, '联想笔记本电脑小新14超薄本 高性能标压英特尔酷睿i5 14英寸轻薄本 16G 512G防眩光屏 灰 办公学生',
     'https://item.jd.com/100057677955.html?extension_id=eyJhZCI6IiIsImNoIjoiIiwic2hvcCI6IiIsInNrdSI6IiIsInRzIjoiIiwidW5pcWlkIjoie1wiY2xpY2tfaWRcIjpcIjkwNWIwZGZkLTZmYTktNDZkOS1hYmU4LTdkYmRiZmNlOGU3N1wiLFwicG9zX2lkXCI6XCIyNjE3XCIsXCJzaWRcIjpcImVjNWYwNzQ3LTI0ZjUtNDJiYy05MWQwLTA4YWVmNDMyMTFlYlwiLFwic2t1X2lkXCI6XCIxMDAwNTc2Nzc5NTVcIn0ifQ==&jd_pop=905b0dfd-6fa9-46d9-abe8-7dbdbfce8e77',
     3498.00,'联想'),
    (2, 'ThinkPad 联想ThinkBook X 2024AI旗舰本 英特尔Evo酷睿Ultra标压处理器 13.5英寸高端商务商旅轻薄笔记本 爆款Ultra9 32G 1T 02CD触屏',
     'https://item.jd.com/10099946189189.html?extension_id=eyJhZCI6IjI2OCIsImNoIjoiMiIsInNrdSI6IjEwMDk5OTQ2MTg5MTg5IiwidHMiOiIxNzMxMjQyMDc2IiwidW5pcWlkIjoie1wiY2xpY2tfaWRcIjpcIjkxZDUzYzlkLTBlMzgtNGJmYS05ODNjLThlYzZkMTVjNjc3MlwiLFwibWF0ZXJpYWxfaWRcIjpcIjM2MDA0MDg5MjU5XCIsXCJwb3NfaWRcIjpcIjI2OFwiLFwic2lkXCI6XCI4NjdjMDZiMC0xODliLTQ3ZWUtODcxNi04Y2FlNjA1Mjk4NWFcIn0ifQ==&jd_pop=91d53c9d-0e38-4bfa-983c-8ec6d15c6772&abt=0',
     8998.00, '联想'),
    (3,'联想（Lenovo）拯救者R9000P 16英寸电竞游戏本笔记本电脑(R9-7945HX 16G 1T RTX4070 2.5K 240Hz100%DCI-P3)灰',
'https://item.jd.com/100147362862.html?extension_id=eyJhZCI6IjI2OCIsImNoIjoiMiIsInNrdSI6IjEwMDE0NzM2Mjg2MiIsInRzIjoiMTczMTI0MjE0OSIsInVuaXFpZCI6IntcImNsaWNrX2lkXCI6XCI5YTZlMzA5Yy1jNDg2LTRhNzgtODlmMi0zMTQwNmQ1ZjkxM2VcIixcIm1hdGVyaWFsX2lkXCI6XCIzNjI2NTI5MjQxMFwiLFwicG9zX2lkXCI6XCIyNjhcIixcInNpZFwiOlwiODY3YzA2YjAtMTg5Yi00N2VlLTg3MTYtOGNhZTYwNTI5ODVhXCJ9In0=&jd_pop=9a6e309c-c486-4a78-89f2-31406d5f913e&abt=0',
10499.00 ,'联想'),

    (4,'联想笔记本电脑小新Pro14 2024 高性能标压酷睿Ultra5 14英寸AI轻薄本 32G 1T 2.8K高刷屏 游戏 灰',
     'https://item.jd.com/100109152429.html?extension_id=eyJhZCI6IiIsImNoIjoiIiwic2hvcCI6IiIsInNrdSI6IiIsInRzIjoiIiwidW5pcWlkIjoie1wiY2xpY2tfaWRcIjpcImU2NDBmZDJjLTM4YWMtNGNjNi05NDcwLWU3YzgyMzVjNzAyM1wiLFwicG9zX2lkXCI6XCIyNjE3XCIsXCJzaWRcIjpcImVjNWYwNzQ3LTI0ZjUtNDJiYy05MWQwLTA4YWVmNDMyMTFlYlwiLFwic2t1X2lkXCI6XCIxMDAxMDkxNTI0MjlcIn0ifQ==&jd_pop=e640fd2c-38ac-4cc6-9470-e7c8235c7023',
5799.00,'联想'),

    (5,'ThinkPad联想E16笔记本电脑 E15升级版 16英寸商务办公学生轻薄本 AI 2024英特尔酷睿Ultra处理器可选 黑色 i7-13700H 32G 1TB 07CD',
     'https://item.jd.com/10088560496212.html?extension_id=eyJhZCI6IiIsImNoIjoiIiwic2hvcCI6IiIsInNrdSI6IiIsInRzIjoiIiwidW5pcWlkIjoie1wiY2xpY2tfaWRcIjpcIjdkODFmYmZiLTY1ZTYtNGQxNy05NTJmLTg3NDI4YzFlZGVlOVwiLFwicG9zX2lkXCI6XCIyNjE3XCIsXCJzaWRcIjpcImVjNWYwNzQ3LTI0ZjUtNDJiYy05MWQwLTA4YWVmNDMyMTFlYlwiLFwic2t1X2lkXCI6XCIxMDA4ODU2MDQ5NjIxMlwifSJ9&jd_pop=7d81fbfb-65e6-4d17-952f-87428c1edee9',
     6979.00,'联想')


]

for record in mock_data:
    cursor.execute('''
    INSERT INTO product (id, product_title, product_link, product_price, product_brand)
    VALUES (?, ?, ?, ?, ?)
    ''', record)

# 提交事务
conn.commit()
