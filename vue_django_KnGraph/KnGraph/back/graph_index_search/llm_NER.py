from typing import List
from langchain_community.vectorstores.neo4j_vector import remove_lucene_chars
from langchain_core.prompts import ChatPromptTemplate
from openai import BaseModel
from pydantic import Field
from langchain_community.chat_models import ChatZhipuAI
from langchain.graphs import Neo4jGraph


llm = ChatZhipuAI(zhipuai_api_key='ed23925e82274091b878af5bb092c261.Bno6aFYOCMhIy1si',model_name="glm-4",temperature=0.5,)
graph = Neo4jGraph(
    url='bolt://localhost:7687',
    username = 'neo4j',
    password = '12345678'
)

# 从文本中提取实体
class Entities(BaseModel):
    """识别实体相关信息。"""
    names: List[str] = Field(
        ...,
        description="文本中出现的问题对象的名称",
    )

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "您正在从文本中提取问题对象。"
            "如‘解释下指针’,问题对象为指针,",
        ),
        (
            "human",
            "请按照给定格式从以下输入中提取信息：{question}",
        ),
    ]
)

entity_chain = prompt | llm.with_structured_output(Entities)


graph.query(
    "CREATE FULLTEXT INDEX entity IF NOT EXISTS FOR (e:知识点|节|章) ON EACH [e.name]")

def generate_full_text_query(input: str) -> str:
    """
    为给定的输入字符串生成全文搜索查询。

    该函数构建一个适用于全文搜索的查询字符串。它通过将输入字符串分割成单词，并对每个单词附加一个相似性阈值（允许2个字符变化），然后使用 AND 运算符将它们组合起来。这对于将用户问题中的实体映射到数据库值非常有用，并且能够容忍一些拼写错误。
    """
    full_text_query = ""
    words = [word for word in remove_lucene_chars(input).split() if word]
    for word in words[:-1]:
        full_text_query += f"{word} AND"
    full_text_query += f"{words[-1]}"
    return full_text_query.strip()

def e_score_retriever(question: str) -> str:
    """
    收集问题中提到的实体的邻域信息
    """
    result = ""
    entities = entity_chain.invoke({"question": question})
    for entity in entities.names:
        response = graph.query(
            """CALL db.index.fulltext.queryNodes('entity', $query, {limit:1}) YIELD node, score
                     RETURN node.name, score""",
            {"query": generate_full_text_query(entity)},
        )

    return response[0]['node.name'],response[0]['score']

