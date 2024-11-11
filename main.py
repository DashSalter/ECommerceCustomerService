import os

import gradio as gr
import time
from src import (
    LLM, ProblemTypeClassification,
    KnowledgeManager, KnowledgeType,
    tools
)

# 代理设置
proxy_url = 'http://127.0.0.1'
proxy_port = '7890'  # 代理的端口
os.environ['http_proxy'] = f'{proxy_url}:{proxy_port}'
os.environ['https_proxy'] = f'{proxy_url}:{proxy_port}'

# 设置模型参数
maximum_length: int = 850  # chatbot的最大回复长度
default_temperature: float = 1.0  # 温度 0.0-2.0
model: str = "gpt-4o-mini"
model_output_speed = 0.01  # 模型输出速度


class GUI:
    llm = LLM()  # 语言模型
    problem_type_classification = ProblemTypeClassification()  # 问题类型分类器
    knowledge_manager = KnowledgeManager()  # 知识库管理器

    def __init__(self):
        self.chatbot = gr.ChatInterface(self.slow_echo, title='电商智能客服系统', type="messages")
        self.data_classifier = False  # 是否使用数据分类器,可以先识别问题类型，再选择知识库

    def slow_echo(self, question, __history, max_length_: int = maximum_length, temperature_: float = 1):
        """模型回复"""
        if self.data_classifier:  # 问题进础分类
            question_type_: list = self.problem_type_classification.classify(question, __history)
        else:  # 使用所以的知识库
            question_type_ = [type_.value for type_ in KnowledgeType]

        # 根据问题类型选择知识库，并整理查询结果
        query_results = self.knowledge_manager.get_query_results(question, question_type_)
        query_results = [i for i in query_results['documents']]

        # 使用LLM模型生成回复
        response = self.llm.invoke(
            question, query_results, model=model,
            max_length=max_length_, temperature=temperature_,
            tools=tools
        )

        # 流式回复结果
        answer = response["answer"]
        for i in range(len(answer)):
            time.sleep(model_output_speed)
            yield answer[: i + 1]

    def run(self) -> None:
        self.chatbot.launch(share=True)


if __name__ == '__main__':
    GUI().run()
    # 我需要一台联想笔记本电脑，价格大概在9000
    # 定制商品是怎么样的呢？还有退货退款规定
