from langchain_community.chat_models import ChatZhipuAI
from langchain.chains import GraphCypherQAChain
from langchain.graphs import Neo4jGraph
from langchain.prompts.prompt import PromptTemplate
from KnGraph.back.graph_index_search.llm_NER import e_score_retriever
from KnGraph.back.graph_CRUD.neo4j_graph import NeoGraph
from KnGraph.back.change_json import to_dict
import json

llm = ChatZhipuAI(zhipuai_api_key='ed23925e82274091b878af5bb092c261.Bno6aFYOCMhIy1si',model_name="glm-4",temperature=0.5,)

graph = Neo4jGraph(
    url='bolt://localhost:7687',
    username = 'neo4j',
    password = '2206040208'
)
graph_se = NeoGraph()

CYPHER_GENERATION_TEMPLATE = """
Task:Generate 生成 Cypher 语句以查询图形数据库.
Instructions:
仅使用架构中提供的关系类型和属性。请勿使用未提供的任何其他关系类型或属性，永远不要返回embedding属性。
Schema:
{schema}

以下为Cypher语句的模版，严格按照模版内容，不得添加任何其他语句
Cypher语句不要return 模版外的其他内容
提问某个知识点到包含什么，用contain关系，提问的实体不用加任何标签，实体语言为提问的语言
Cypher examples:
# 常量包含什么内容
MATCH (s{{name:'常量'}})-[rel:contain]->(n)
RETURN n
只返回n的name属性不返回其他内容

提问到某知识点是什么意思或某知识点的定义是什么，得到该知识点的desc属性，用contain关系找的包含的节点，再得到包含节点的desc属性,按照模版，不得加任何其他的语句
Cypher examples:
# 文件引入是什么意思 或 文件引入的定义
MATCH (p{{name:'文件引入'}}) RETURN p.desc AS desc
UNION
MATCH (n1{{name:'文件引入'}}) - [rel:contain] -> (n2) RETURN n2.desc AS desc

提问到某知识点前继，后继，前置，后置知识,按照模版，不得加任何其他的语句
当前例子，关系只有follow_up 没有其他任何关系
Cypher examples:
# 指针的前置知识
MATCH (p{{name:'指针'}}) -[rel:follow_up]->(n) return n.name AS name
UNION
MATCH (p{{name:'指针'}}) <-[rel:follow_up]- (n) return n.name AS name
严格按照此语句，不得增添语句


Note: 请勿在回复中包含任何解释或道歉。不要回答任何可能提出其他问题的问题，除非你构建一个 Cypher 语句。请勿包含除生成的 Cypher 语句之外的任何文本。

The question is:
{question}"""

CYPHER_GENERATION_PROMPT = PromptTemplate(
    input_variables=["schema", "question"], template=CYPHER_GENERATION_TEMPLATE
)

def graph_inf_chain(question):
    chain = GraphCypherQAChain.from_llm(
        llm, graph=graph, verbose=True, allow_dangerous_requests=True,
        cypher_prompt=CYPHER_GENERATION_PROMPT,
        return_direct=True,
        return_intermediate_steps=True
    )
    e, score = e_score_retriever(question)
    res = graph_se.find_by_e1(e)
    print(e)
    res_dict = to_dict(res)
    node_data = json.loads(res_dict)['data']
    list = []
    for i in node_data:
        dic = {"name":i['name'],"desc": i['desc']}
        list.append(dic)

    try:
        answer = chain.invoke(question)
    except Exception as e:
        return list,None,res_dict
    else:
        cypher = answer['intermediate_steps']
        res = answer['result']
        if len(res) == 0:
            return list,None,res_dict
        else:
            return res,cypher,res_dict

if __name__ == "__main__":
    print(graph_inf_chain('我想学变量'))