from typing import Iterable

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages import AIMessageChunk
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import AddableDict
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables.utils import Output
from langchain_openai import ChatOpenAI
from .tools import tool_dict


class LLM:
    _chat_history = ChatMessageHistory()  # 对话历史

    def __init__(self, chat_history_max_length: int = 20):
        self.chat_history_max_length: int = chat_history_max_length
        self.knowledge_prompt = None  # 问答模板
        self.create_chat_prompt()  # 创建聊天模板

    def create_chat_prompt(self) -> None:
        # AI系统prompt
        knowledge_system_prompt = """
        你叫小琳，是一位电商客服助手，主要帮助客户解决问题，和帮客户推荐商品
        推荐商品例如如:向客户提供产品名称、价格,跳转链接等信息。还有解答售后政策，协助解决售后问题。
        
        1.客户向你打招呼时，请介绍自己和说明自己可以帮助客户搜索产品和解决售后问题。
        2.如果客户询问电商以外的问题，请引导回有关产品信息或服务的相关信息。如果没有搜索到相关的产品信息或服务，就说‘不好意思，没有找到相关的产品信息或服务。’
        3.如果客户要求推荐商品，请询问商品的名称和价位。
        4.回复客户的时候，尽量格式整齐一些，将数据信息清晰详细地呈现出来。
        
        如果产品需要进行退货/维修/推荐/查询商品等的服务，使用检索到的上下文来回答问题。\n\n"
        "{context}"
        """

        # 没有指定知识库的模板的AI系统模板
        self.knowledge_prompt = ChatPromptTemplate.from_messages(  # 正常prompt
            [
                ("system", knowledge_system_prompt),
                ("placeholder", "{chat_history}"),
                ("human", "{input}"),
            ]
        )

    @staticmethod
    def streaming_parse(chunks: Iterable[AIMessageChunk]) -> list[AddableDict]:
        """统一模型的输出格式，将模型的输出存储到字典answer的value中"""
        for chunk in chunks:
            yield AddableDict({'answer': chunk.content})

    def history_message_model(self, rag_chain) -> RunnableWithMessageHistory:
        """添加对话历史"""
        return RunnableWithMessageHistory(  # 可用于任何的chain中添加对话历史，将以下之一作为输入
            rag_chain,  # 传入聊天链
            lambda session_id: self._chat_history,  # 传入历史信息
            input_messages_key="input",  # 输入信息的键名
            history_messages_key="chat_history",  # 历史信息的键名
            output_messages_key="answer",  # 输出答案
        )

    def get_chain(self, model: str, max_length: int, temperature: float) -> RunnableWithMessageHistory:
        """获取聊天链"""
        # 只保留指定的知识库个记录
        chat = ChatOpenAI(model=model, max_tokens=max_length, temperature=temperature)
        rag_chain = self.knowledge_prompt | chat | self.streaming_parse
        return self.history_message_model(rag_chain)

    def function_call(self, model: str, max_length: int, temperature: float, tools: list) -> RunnableWithMessageHistory:
        """函数调用确认"""
        chat = ChatOpenAI(model=model, max_tokens=max_length, temperature=temperature)
        llm_with_tools = chat.bind_tools(tools)
        rag_chain = self.knowledge_prompt | llm_with_tools
        return self.history_message_model(rag_chain)

    def invoke(self, question: str, query_results, model="gpt-3.5-turbo",
               max_length=256, temperature=1, tools: list = None) -> Output:
        """
        :param tools: 工具集合
        :param query_results: # 知识库查询结果
        :param question: 用户提出的问题 例如: '请问你是谁？'
        :param model: 使用模型,默认为 'gpt-3.5-turbo'
        :param max_length: 数据返回最大长度
        :param temperature: 数据温度值
        """
        self._chat_history.messages = self._chat_history.messages[-self.chat_history_max_length:]

        # function_calling
        function_chat = self.function_call(model, max_length, temperature, tools)
        tool_calls = function_chat.invoke(
            {"input": question, 'context': query_results},
            {"configurable": {"session_id": "unused"}}  # 历史信息存入session_id
        ).tool_calls

        # 回调函数结果
        for tool_call in tool_calls:
            result1 = tool_dict[tool_call['name']].invoke(input=tool_call['args'])
            query_results.append(result1)

        # 根据回调结果生成回复
        chat = self.get_chain(model, max_length, temperature)
        result = chat.invoke(
            {"input": question, 'context': query_results},
            {"configurable": {"session_id": "unused"}}
        )
        print('-' * 50)
        print('RAG+function_chat:', query_results)
        print('result:', result)
        print('-' * 50)
        return result

    def clear_history(self) -> None:
        """清除历史信息"""
        self._chat_history.clear()

    def get_history_message(self) -> list:
        """获取历史信息"""
        return self._chat_history.messages
