from langchain_community.chat_models import ChatZhipuAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
import json

from KnGraph.back import NeoGraph
from KnGraph.back.RAG.serch_rag import RagSearch
from KnGraph.back.graph_index_search.llm_generate_cypher import graph_inf_chain

llm = ChatZhipuAI(zhipuai_api_key='ed23925e82274091b878af5bb092c261.Bno6aFYOCMhIy1si',model_name="glm-4")

store = {}


def retriever(question: str):
    rag = RagSearch()

    global rag_data,graph_data,cypher,graph_for_echarts
    rag_data = rag.get_relevant_context(question)
    graph_data,cypher,graph_for_echarts = graph_inf_chain(question)
    if cypher is not None:
        cypher = cypher[0]["query"]
    final_data =\
    f"""
    rag数据：
    {rag_data}
    图数据：
    {graph_data}
    """
    return final_data


template = """根据以下上下文回答问题：
{context}

当问到包含什么或包含哪些知识点的内容时，按照图数据的内容回答
问到解释知识点时，结合rag数据与图数据

回答要根据上下文，不知道的不要回答，句数在3到5句，回复要精简

问题：{question}
"""

prompt = ChatPromptTemplate.from_template(template)

chain = (
        RunnableParallel(
            {
                "context": retriever,
                "question": RunnablePassthrough(),
            }
        )
        | prompt
        | llm
        | StrOutputParser()
)

def qa_robot(question):
    qa_answer = chain.invoke(question)

    dic = {"rag_data":rag_data,"graph_data":graph_data,"cypher":cypher,"qa_answer":qa_answer,"graph_for_echarts":json.loads(graph_for_echarts)}
    return dic


if __name__ == '__main__':
    print(qa_robot("变量是什么"))