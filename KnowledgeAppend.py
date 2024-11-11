import os
from dotenv import load_dotenv
from src import KnowledgeManager, KnowledgeType

load_dotenv()

proxy_url = 'http://127.0.0.1'
proxy_port = '7890'  # 代理的端口
os.environ['http_proxy'] = f'{proxy_url}:{proxy_port}'
os.environ['https_proxy'] = f'{proxy_url}:{proxy_port}'

if __name__ == '__main__':
    # doc = DocumentChunker('售后.docx')
    km = KnowledgeManager()

    # km.add_after_sales(doc.load())

    # print(km.collection.get(ids=['after_sales:1']))

    results = km.collection.query(
        query_embeddings=km.vector_store.embed_query('食品类商品售后'),  # 特殊商品售后服务规定
        n_results=1,  # 返回结果数
        where={"source": KnowledgeType.AFTER_SALES.value},  # 指定知识库
        # where={"source": {"$in": search_types}},   # 指定搜索类型
        # search_types = [KnowledgeType.AFTER_SALES.value, KnowledgeType.OTHER_TYPE.value]
    )
    print(results)
