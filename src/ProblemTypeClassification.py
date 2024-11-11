from langchain_openai import ChatOpenAI
from langchain.output_parsers import CommaSeparatedListOutputParser
import os
from langchain.prompts import PromptTemplate
from .KnowledgeType import KnowledgeType

proxy_url = 'http://127.0.0.1'
proxy_port = '7890'  # 代理的端口
os.environ['http_proxy'] = f'{proxy_url}:{proxy_port}'
os.environ['https_proxy'] = f'{proxy_url}:{proxy_port}'


class ProblemTypeClassification:
    def __init__(self):
        """根据问题来选择向量数据库"""
        self.chat = ChatOpenAI(model='gpt-3.5-turbo', max_tokens=500, temperature=0)
        self.list_output_parser = CommaSeparatedListOutputParser()
        self.prompt = PromptTemplate(
            template="我将给出一下对话的场景和当前用户提供的问题，对话场景:{char_history}\n"
                     "问题:{question}. \n"
                     f"请根据以上的问题，对问题进行分类:{','.join([type_.value for type_ in KnowledgeType])}\n"
                     "输出格式:{format_instructions}. ",
            input_variables=["question"],
            partial_variables={"format_instructions": self.list_output_parser.get_format_instructions()}
        )

    def classify(self, question_: str, char_history: dict) -> list:
        """解析问题并返回分类结果"""
        prompt = self.prompt.format(question=question_, char_history=char_history)
        print(prompt)
        response = self.chat.invoke(prompt)
        return self.list_output_parser.parse(response.content)


if __name__ == '__main__':
    from dotenv import load_dotenv

    load_dotenv()

    problem_type_classification = ProblemTypeClassification()
    question = "我想买一台电脑"
    print(problem_type_classification.classify(question))
