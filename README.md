# 智能电商客服系统
智能电商客服系统(ECommerceCustomerService)

系统介绍:
智能电商客服系统是为电商用户提供的在线服务系统，主要负责在线接待客户，解答疑问，处理销售及售后问题。
解决问题主要包括以下:
- 产品信息提供：向客户提供产品详情、规格、价格等信息。
- 售后服务: 解答售后政策，协助解决售后问题。


## 项目结构搭建

### python版本要求
```text
Python version==3.10
```
###


#### Model Url(需要下载的模型文件)
```text
链接：https://pan.baidu.com/s/1aiq6AS1ucAs_AX9-Wn_klQ?pwd=ARAR 
提取码：ARAR
```
###

#### 项目环境文件.env文件(openai_key)
需要在项目中创建.env文件，配置以下信息
```text
OPENAI_API_KEY = ""
OPENAI_BASE_URL = "https://api.openai.com/v1/"
```
###

解决方案
"""
```python
from unstructured.file_utils.filetype import FileType, detect_filetype
#detect_filetype 函数中的 361行加上以下代码
if LIBMAGIC_AVAILABLE:
    import magic

    mime_type = (

# 修改成以下代码
if LIBMAGIC_AVAILABLE:
    import locale
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

    import magic

    mime_type = (
    
```


