from py2neo import *

class NeoGraph:
    def __init__(self):
        self.graph = Graph('bolt://localhost:7687', auth=('neo4j', '2206040208'))


    # 关系查询:实体1
    def find_by_e1(self, entity1, min_l=1, max_l=1, limit=25):
        answer = self.graph.run(
            f"MATCH (n1{{name: $entity1}}) - [rel*{min_l}..{max_l}] -> (n2) return rel LIMIT {limit}",
            entity1=entity1).data()
        return answer

    # 关系查询：实体1+关系
    def find_by_e1_rel(self,entity1,relation,min_l=1,max_l=1,limit=25):
        answer = self.graph.run(f"MATCH (n1{{name: $entity1}}) - [rel:{relation}*{min_l}..{max_l}] -> (n2) return rel LIMIT {limit}",entity1=entity1).data()
        return answer

    # 关系查询 整个知识图谱体系
    def find_all(self):
        answer = self.graph.run("MATCH (n1)- [rel] -> (n2) RETURN rel").data()
        return answer

    # 关系查询 实体2
    def find_by_e2(self, entity2, min_l=1, max_l=1, limit=25):
        answer = self.graph.run(
            f"MATCH (n1) - [rel*{min_l}..{max_l}] -> (n2{{name: $entity2}}) return rel LIMIT {limit}",
            entity2=entity2).data()
        return answer

    # 关系查询：实体2+关系
    def find_by_e2_rel(self, entity2,relation, min_l=1, max_l=1, limit=25):
        answer = self.graph.run(
            f"MATCH (n1) - [rel:{relation}*{min_l}..{max_l}] -> (n2{{name: $entity2}}) return rel LIMIT {limit}",
            entity2=entity2).data()
        return answer

    #关系查询：实体1 + 实体2
    def find_by_e1_e2(self, entity1, entity2, min_l=1, max_l=10, limit=25):
        answer = self.graph.run(
            f"MATCH (n1{{name: $entity1}}) - [rel*{min_l}..{max_l}] - (n2{{name: $entity2}}) "
            f"RETURN n1, rel, n2 LIMIT {limit}",
            entity1=entity1,
            entity2=entity2).data()
        return answer


