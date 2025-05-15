import json
import pandas as pd
from py2neo import Graph,Relationship,Node,NodeMatcher

des = pd.read_excel('data/知识点描述.xlsx')

# 连接数据库,数据库对象为: graph
graph = Graph('neo4j://localhost:7687',auth=('neo4j','12345678'))
# 删除所有节点
graph.delete_all()
# 导入节点
with open('data\\chapter.json',encoding='UTF-8') as f:
    file = json.loads(f.read())
    for word in file:
        node = Node('章',name=word)
        graph.create(node)

with open('data\\section.json',encoding='UTF-8') as f:
    file = json.loads(f.read())
    for word in file:
        node = Node('节',name=word)
        graph.create(node)

with open('data\\point.json',encoding='UTF-8') as f:
    file = json.loads(f.read())
    for word in file:
        desc = des.loc[des['name'] == word]['des'].values[0]
        node = Node('知识点',name=word,desc=desc)
        graph.create(node)

data_re = pd.read_excel('data\\关系.xlsx')

for index,value in data_re.iterrows():
    a = graph.nodes.match('知识点',name=value.iloc[0]).first()
    if a is None:
        a = graph.nodes.match('章',name=value.iloc[0]).first()
        if a is None:
            a = graph.nodes.match('节',name=value.iloc[0]).first()
    b = graph.nodes.match('知识点', name=value.iloc[1]).first()
    if b is None:
        b = graph.nodes.match('章', name=value.iloc[1]).first()
        if b is None:
            b = graph.nodes.match('节', name=value.iloc[1]).first()
    c = value.iloc[2]
    re = Relationship(a, c, b)
    graph.create(re)

