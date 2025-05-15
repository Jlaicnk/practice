import random

import torch
from KnGraph.back.KGE.TransE_train import TransE
import numpy as np
from KnGraph.back.graph_CRUD.Graph_Alter import GraphCRUD

class Recommend:
    def __init__(self):
        self.model_path = "KnGraph/back/KGE/result/best_transe_model.pth"
        self.dict_path = 'KnGraph/back/KGE/data/all_ent.txt'

        self.graphCRUD = GraphCRUD()

        self.model = TransE(num_entities=168,
                       num_relations=3,
                       embedding_dim=200,
                       margin=1.5,
                       norm=True)
        self.model.load_state_dict(torch.load(self.model_path))
        self.entity_emb = self.model.entity_emb.weight.data
        self.model.eval()


        self.entity_to_id = {}
        self.id_to_entity = {}
        with open(self.dict_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line:  # 确保行不为空
                    key, value = line.split()
                    self.entity_to_id[key] = int(value)
                    self.id_to_entity[int(value)] = key



    def get_interacted_id(self,interacted_list):
        interacted_ids = []
        for i in interacted_list:
            interacted_ids.append(self.entity_to_id[i])
        return interacted_ids

    def get_user_embedding(self,interacted_list):
        interacted_id = self.get_interacted_id(interacted_list)
        interacted_emb = self.entity_emb[torch.LongTensor(interacted_id)]
        return torch.mean(interacted_emb, dim=0)

    def get_recommend_list(self,interacted_list, k):
        user_emb = self.get_user_embedding(interacted_list)

        scores = torch.matmul(user_emb, self.entity_emb.T)

        interacted_ids = self.get_interacted_id(interacted_list)
        scores[interacted_ids] = -np.inf

        # 获取Top-K推荐
        top_k_scores, top_k_ids = torch.topk(scores, k)

        return [[self.id_to_entity[i.item()], s.item()] for i, s in zip(top_k_ids, top_k_scores.data)]

    def get_recommend_item(self, interacted_list, k=10):
        recommend_list = self.get_recommend_list(interacted_list, k)
        item_list = []
        for name, score in recommend_list:
            res = self.graphCRUD.search_info(node_name=name)
            res_belong = self.graphCRUD.search_belong(name)

            count = random.randint(10, 100)
            name = res['name']

            if res_belong:
                belong_name = res_belong[0]['source.name']
            else:
                belong_name = name

            if 'desc' in res:
                desc = res['desc']
            else:
                desc = ''
            item_dict = {'name': name, 'belong': belong_name, 'desc': desc, 'count': count}
            item_list.append(item_dict)

        return item_list

if __name__ == '__main__':
    interact_list = ['变量','指针','文件','文件引入','文本文件与二进制文件','文件操作','文件随机读写','字符文件读写函数']
    re = Recommend()
    print(re.get_recommend_item(interact_list,10))



# def get_interacted_id(user_id):
#         data_path = "data/index_rel_triple.txt"
#         interacted_ids = []
#         with open(data_path, 'r', encoding='utf-8') as file:
#                 for line in file:
#                     line = line.strip()
#                     if line:  # 确保行不为空
#                         head, rel, tail = line.split()
#                         if int(head) == user_id:
#                                 interacted_ids.append(int(tail))
#         return interacted_ids
