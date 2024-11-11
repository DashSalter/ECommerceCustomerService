import chromadb
from langchain_openai import OpenAIEmbeddings


class VectorStore:
    vector_store_path = './vector_store'  # 向量数据库的路径
    vector_store_collection = 'ECommerceCustomerService'  # 向量数据库的集合名称

    def __init__(self) -> None:
        self.client = chromadb.PersistentClient(path=self.vector_store_path)
        self.embeddings = OpenAIEmbeddings()

    def create_collection(self, collection_: str = None) -> chromadb.Collection:
        """创建集合"""
        if collection_ is None:
            collection_ = self.vector_store_collection
        return self.client.get_or_create_collection(name=collection_)

    def get_collection(self, collection_: str = None) -> chromadb.Collection:
        """获取集合"""
        return self.create_collection(collection_)

    def get_collection_names(self) -> list:
        """获取集合列表"""
        return [i.name for i in self.client.list_collections()]

    def embed_documents(self, list_texts: list[str]) -> list[list[float]]:
        """获取文本的向量"""
        return self.embeddings.embed_documents(list_texts)

    def embed_query(self, query: str) -> list[float]:
        """获取查询语句的向量"""
        return self.embeddings.embed_query(query)


if __name__ == '__main__':
    import time
    import os

    proxy_url = 'http://127.0.0.1'
    proxy_port = '7890'  # 代理的端口
    os.environ['http_proxy'] = f'{proxy_url}:{proxy_port}'
    os.environ['https_proxy'] = f'{proxy_url}:{proxy_port}'

    start_time = time.time()
    from dotenv import load_dotenv

    load_dotenv()
    VectorStore.vector_store_path = '../vector_store'  # 向量数据库的路径
    vector_store = VectorStore()
    print(f"--- {time.time() - start_time} VectorStore ---")

    start_time = time.time()
    collection = vector_store.get_collection()
    print(f"--- {time.time() - start_time} get_collection ---")

    start_time = time.time()
    print(vector_store.embed_documents(['我爱你', '你爱我']))
    print(f"--- {time.time() - start_time} embed_documents ---")

    start_time = time.time()
    print(vector_store.embed_query('你爱我吗'))
    print(f"--- {time.time() - start_time} embed_query ---")
