from enum import Enum

class KnowledgeType(Enum):
    AFTER_SALES: str = 'after_sales'  # 售后
    PRE_SALES: str = 'pre_sales'  # 售前
    # PRODUCTS: str = 'products'  # 产品
    OTHER: str = 'other'  # 其他