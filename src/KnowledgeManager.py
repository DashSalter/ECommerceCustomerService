import os
from dotenv import load_dotenv
from src import VectorStore, DocumentChunker, KnowledgeType
from chromadb import QueryResult

load_dotenv()

proxy_url = 'http://127.0.0.1'
proxy_port = '7890'  # 代理的端口
os.environ['http_proxy'] = f'{proxy_url}:{proxy_port}'
os.environ['https_proxy'] = f'{proxy_url}:{proxy_port}'


class KnowledgeManager:
    def __init__(self):
        """用于后台添加向量问答知识库"""
        self.vector_store = VectorStore()
        self.collection = self.vector_store.get_collection()

    def _collection_add(self, documents, ids=None, source=None) -> None:
        """向量问答知识库添加数据"""

        if hasattr(documents[0], 'page_content'):
            documents = [document.page_content for document in documents]

        if ids is None:
            ids = [f'{source}:{i}' for i in range(len(documents))]

        self.collection.add(
            ids=ids,
            documents=documents,
            metadatas=[{'source': source} for _ in range(len(documents))],
            embeddings=self.vector_store.embed_documents(documents)
        )

    def add_after_sales(self, documents:list, ids=None, source=KnowledgeType.AFTER_SALES.value) -> None:
        """添加售后信息"""
        self._collection_add(documents, ids, source)

    def add_pre_sale(self, documents, ids=None, source=KnowledgeType.PRE_SALES.value) -> None:
        """添加售前信息"""
        self._collection_add(ids, documents, source)

    # def add_products(self, documents, ids=None, source=KnowledgeType.PRODUCTS.value) -> None:
    #     """添加产品信息"""
    #     self._collection_add(ids, documents, source)

    def get_query_results(self, query: str, knowledge_type: list, top_k: int = 2) -> QueryResult:
        """获取检索数据"""
        return self.collection.query(
            query_embeddings=self.vector_store.embed_query(query),  # 特殊商品售后服务规定
            n_results=top_k,  # 返回结果数
            where={"source": {"$in": knowledge_type}},  # 指定知识库
        )


if __name__ == '__main__':
    # doc = DocumentChunker('售后.docx')
    km = KnowledgeManager()

    # km.add_after_sales(doc.load())

    # print(km.collection.get(ids=['after_sales:1']))

    results = km.collection.query(
        query_embeddings=km.vector_store.embed_query('食品类商品售后'),  # 特殊商品售后服务规定
        n_results=1,  # 返回结果数
        where={"source": KnowledgeType.AFTER_SALES.value},  # 指定知识库
    )
    print(results)
