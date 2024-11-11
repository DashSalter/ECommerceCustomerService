from langchain_core.tools import tool

import sqlite3


@tool
def search_products(product_brand: str, product_price_range: int, limit: int = 3) -> str:
    """
    查询商品信息和给客户推荐商品，需要根据产品品牌和价格范围搜索产品详细信息。
    :param product_brand: 商品的品牌
    :param product_price_range: 商品的价格 如100
    :param limit: 默认返回3条结果
    :return: 商品的详细信息
    """
    # 连接到数据库
    conn = sqlite3.connect('product_db.db')
    cursor = conn.cursor()

    # 构建查询语句
    query = """
    SELECT * FROM product 
    WHERE product_title LIKE ? 
    AND product_price BETWEEN ? AND ?
    LIMIT ?
    """

    # 执行查询
    cursor.execute(query, (f'%{product_brand}%', product_price_range * 0.9, product_price_range * 1.1, limit))

    # 获取所有匹配的产品
    results = cursor.fetchall()

    # 关闭连接
    conn.close()

    # 格式化结果为字符串
    if results:
        formatted_results = '\n'.join([f"相关商品: Title: {r[1]}, Link: {r[2]}, Price: {r[3]}, Brand: {r[4]}" for r in results])
        return formatted_results
    else:
        return "相关商品:无"


tools = [search_products]

tool_dict = {getattr(t, 'name'): t for t in tools}

if __name__ == '__main__':
    # print(search_products(product_name='联想', product_price_range= 9000))
    # print(search_products(**{"product_name":"联想","product_price_range":9000}))

    print(tool_dict)
