from py2neo import Graph,Relationship,Node,NodeMatcher
from langchain_neo4j import Neo4jGraph
import pandas as pd

class GraphCRUD:
    def __init__(self):
        self.graph = Graph('neo4j://localhost:7687',auth=('neo4j','12345678'))
        self.langGraph = Neo4jGraph(
            url='bolt://localhost:7687',
            username = 'neo4j',
            password = '12345678'
        )

    def create_node(self,node:dict):
        matcher = NodeMatcher(self.graph)

        node_name = node["name"]
        res = matcher.match(name=node_name).first()
        if res is not None:
            return

        node_label = node["label"]
        node_desc = node["desc"]

        c_node = Node(node_label, name=node_name, desc=node_desc)
        self.graph.create(c_node)

    def create_rel(self,head:dict,rel:str,tail:dict):
        matcher = NodeMatcher(self.graph)
        head_name = head["name"]
        head_node = matcher.match(name=head_name).first()

        if head_node is None:
            head_label = head["label"]
            if "desc" in head:
                head_desc = head["desc"]
            else:
                head_desc = ""
            head_node = Node(head_label, name=head_name, desc=head_desc)
            self.graph.create(head_node)

        tail_name = tail["name"]
        tail_node =  matcher.match(name=tail_name).first()

        if tail_node is None:
            tail_label = tail["label"]
            if "desc" in tail:
                tail_desc = tail["desc"]
            else:
                tail_desc = ""
            tail_node = Node(tail_label, name=tail_name, desc=tail_desc)
            self.graph.create(tail_node)

        re = Relationship(head_node,rel,tail_node)
        self.graph.create(re)

    def update(self,node_before_name,node_after):
        matcher = NodeMatcher(self.graph)

        res = matcher.match(name=node_before_name).first()

        res["name"] = node_after["name"]
        if res["label"]:
            res["label"] = node_after["label"]
        if res["desc"]:
            res["desc"] = node_after["desc"]

        self.graph.push(res)

    def search(self,node_name:str,use_fuzzy_search:bool=False):
        if use_fuzzy_search:
            response = self.langGraph.query(
                """CALL db.index.fulltext.queryNodes('entity', $query, {limit:1}) YIELD node, score
                     RETURN node.name""",
                {"query": node_name},)
            res = response[0]["node.name"]

        else:
            matcher = NodeMatcher(self.graph)
            response = matcher.match(name=node_name).first()
            if response:
                res = response['name']
            else:
                res = None

        print(res)

    def search_info(self,node_name:str,use_fuzzy_search:bool=False):
        if use_fuzzy_search:
            response = self.langGraph.query(
                """CALL db.index.fulltext.queryNodes('entity', $query, {limit:1}) YIELD node, score
                     RETURN node""",
                {"query": node_name},)
            res = response[0]['node']

        else:
            matcher = NodeMatcher(self.graph)
            response = matcher.match(name=node_name).first()
            if response:
                res = response
            else:
                res = None

        return res

    def delete_node(self,node_name):
        matcher = NodeMatcher(self.graph)
        node = matcher.match(name=node_name).first()
        if node is not None:
            self.graph.delete(node)
            return True
        else:
            return False

    def delete_rel(self,head_name,rel,tail_name):
        matcher = NodeMatcher(self.graph)
        head_node = matcher.match(name=head_name).first()
        tail_name = matcher.match(name=tail_name).first()
        rels = self.graph.relationships.match(nodes=(head_node, tail_name), r_type=rel)
        if rels is not None:
            for rel in rels:
                self.graph.separate(rel)
            return True
        else:
            return False

    def create_csv_node(self,node_csv):
        try:
            df = pd.read_csv(node_csv,encoding='GBK')
            for index, row in df.iterrows():
                node = {
                    "name": row["name"],
                    "label": row["label"],
                    "desc": row["desc"]
                }
                self.create_node(node)
            print("节点已成功创建")
        except FileNotFoundError:
            print("文件未找到")
        except Exception as e:
            print(f"处理 CSV 文件时出错: {e}")

    def create_csv_rel(self,rel_csv):
        try:
            df = pd.read_csv(rel_csv,encoding='utf-8')
            for index, row in df.iterrows():
                head_node = {"name": row["head"]}
                tail_node = {"name": row["tail"]}
                rel = str(row["rel"])
                self.create_rel(head_node,rel,tail_node)
            print("关系已成功创建")
        except FileNotFoundError:
            print("文件未找到")
        except Exception as e:
            print(f"处理 CSV 文件时出错: {e}")

    def delete_csv_node(self,node_csv):
        try:
            df = pd.read_csv(node_csv,encoding='GBK')
            for index, row in df.iterrows():
                name = row["name"]
                self.delete_node(name)
            print("节点已删除")
        except FileNotFoundError:
            print("文件未找到")
        except Exception as e:
            print(f"处理 CSV 文件时出错: {e}")

    def delete_csv_rel(self,rel_csv):
        try:
            df = pd.read_csv(rel_csv,encoding='GBK')
            for index, row in df.iterrows():
                head_name = row['head']
                tail_name = row['tail']
                rel = str(row['rel'])

                self.delete_rel(head_name,rel,tail_name)
            print("关系已删除")
        except FileNotFoundError:
            print("文件未找到")
        except Exception as e:
            print(f"处理 CSV 文件时出错: {e}")

    def create_by_csv(self,node_csv,rel_csv):
        self.create_csv_node(node_csv)
        self.create_csv_rel(rel_csv)

    def get_entity2id_rel(self):
        entity = self.graph.run("match (n) return n")
        rel = self.graph.run("MATCH (n1)- [rel] -> (n2) RETURN rel").data()

        entity_list = []
        for n in entity:
            node = n['n']
            label = list(node.labels)[0]
            name = node['name']
            desc = node['desc']
            entity_list.append({
                'label':label,
                'name':name,
                'desc':desc
            })
        entity_df = pd.DataFrame(entity_list)
        entity_df.to_csv("data/entity.csv",index=False,encoding='UTF-8')

        rel_list = []
        for r_line in rel:
            rels = [r_line['rel']]
            for r in rels:
                source = r.start_node['name']
                target = r.end_node['name']
                rel = type(r).__name__
                rel_list.append({
                    'head':source,
                    'rel':rel,
                    'tail':target
                })
        rel_df = pd.DataFrame(rel_list)
        rel_df.to_csv("data/rel.csv", index=False, encoding='UTF-8')

    def search_belong(self,node_name):
        res = self.graph.run("""MATCH (source:章)-[*]->(target)
                        where target.name = $query
                        RETURN source.name
                        limit 1""",
                       {"query": node_name})
        return res.data()

    def input_data(self):
        self.graph.delete_all()
        entity = pd.read_csv('data/entity.csv',encoding='UTF-8')
        for index, row in entity.iterrows():
            node = Node(row['label'], name=row['name'],desc=row['desc'])
            self.graph.create(node)
        rel = pd.read_csv('data/rel.csv', encoding='UTF-8')
        for index, row in rel.iterrows():
            head = row['head']
            rel = row['rel']
            tail = row['tail']
            a = self.graph.nodes.match('知识点', name=head).first()
            if a is None:
                a = self.graph.nodes.match('章', name=head).first()
                if a is None:
                    a = self.graph.nodes.match('节', name=head).first()
            b = self.graph.nodes.match('知识点', name=tail).first()
            if b is None:
                b = self.graph.nodes.match('章', name=tail).first()
                if b is None:
                    b = self.graph.nodes.match('节', name=tail).first()
            re = Relationship(a, rel, b)
            self.graph.create(re)
        # self.create_csv_rel('data/rel.csv')

if __name__ == '__main__':
    GraphCRUD = GraphCRUD()
    node_before = "123456"
    node_after = {'name':'变量'}
    head_node = {'name':"新建的头结点",'label':'测试'}
    tail_node = {'name':"新建的尾结点",'label':'测试'}
    re = '测试关系'
    node_csv = 'input_data/entity.csv'
    rel_csv = 'input_data/rel.csv'
    # GraphCRUD.input_data()
    # GraphCRUD.search_info('构造类型',use_fuzzy_search=False)
    # GraphCRUD.create_by_csv(node_csv, rel_csv)
    # GraphCRUD.delete_csv_node(node_csv)
    # GraphCRUD.delete_csv_rel(rel_csv)
    # GraphCRUD.update(node_before,node_after)
    # GraphCRUD.create_rel(head_node,re,tail_node)
    # GraphCRUD.delete_node('新建的头结点')
    # GraphCRUD.delete_node('新建的尾结点')
    # GraphCRUD.delete_rel('新建的头结点','测试关系','新建的尾结点')


