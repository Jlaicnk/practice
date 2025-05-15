import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import numpy as np
import random
from collections import defaultdict


class TransE(nn.Module):
    def __init__(self, num_entities, num_relations, embedding_dim=100, margin=2.0, norm=True):
        super(TransE, self).__init__()
        self.num_entities = num_entities
        self.num_relations = num_relations
        self.embedding_dim = embedding_dim
        self.margin = margin
        self.norm = norm  # 是否进行L2归一化

        # 初始化实体和关系嵌入
        self.entity_emb = nn.Embedding(num_entities, embedding_dim)
        self.relation_emb = nn.Embedding(num_relations, embedding_dim)

        # Xavier初始化
        nn.init.xavier_uniform_(self.entity_emb.weight.data)
        nn.init.xavier_uniform_(self.relation_emb.weight.data)

    def forward(self, heads, relations, tails):
        # 获取嵌入向量 [batch_size, embedding_dim]
        h = self.entity_emb(heads)
        r = self.relation_emb(relations)
        t = self.entity_emb(tails)

        # L2归一化（可选）
        if self.norm:
            h = F.normalize(h, p=2, dim=1)
            r = F.normalize(r, p=2, dim=1)
            t = F.normalize(t, p=2, dim=1)

        # 计算得分：||h + r - t||₂
        score = torch.norm(h + r - t, p=2, dim=1)
        return score

    def loss(self, pos_scores, neg_scores):
        # 边距损失函数 + L2正则化
        margin_loss = torch.mean(torch.relu(pos_scores - neg_scores + self.margin))
        l2_reg = torch.norm(self.entity_emb.weight, p=2) + torch.norm(self.relation_emb.weight, p=2)
        return margin_loss + 1e-4 * l2_reg


def train_transE(model, train_triplets, all_triplets, num_epochs=100, batch_size=32, lr=0.01, save_path=None):
    optimizer = optim.Adam(model.parameters(), lr=lr)
    triplet_set = set(all_triplets)  # 用于安全负采样

    best_mrr = 0.0
    for epoch in range(num_epochs):
        model.train()
        total_loss = 0.0
        random.shuffle(train_triplets)

        for i in range(0, len(train_triplets), batch_size):
            batch = train_triplets[i:i + batch_size]
            heads = torch.LongTensor([t[0] for t in batch])
            relations = torch.LongTensor([t[1] for t in batch])
            tails = torch.LongTensor([t[2] for t in batch])

            # ----------------- 安全负采样 -----------------
            neg_heads, neg_tails = [], []
            for h, r, t in batch:
                for _ in range(5):  # 最多尝试5次生成有效负样本
                    if random.random() < 0.5:
                        neg_h = random.randint(0, model.num_entities - 1)
                        if (neg_h, r, t) not in triplet_set:
                            neg_heads.append(neg_h)
                            neg_tails.append(t)
                            break
                    else:
                        neg_t = random.randint(0, model.num_entities - 1)
                        if (h, r, neg_t) not in triplet_set:
                            neg_heads.append(h)
                            neg_tails.append(neg_t)
                            break
                else:  # 如果未找到有效负样本，随机生成
                    if random.random() < 0.5:
                        neg_heads.append(random.randint(0, model.num_entities - 1))
                        neg_tails.append(t)
                    else:
                        neg_heads.append(h)
                        neg_tails.append(random.randint(0, model.num_entities - 1))

            neg_heads = torch.LongTensor(neg_heads)
            neg_tails = torch.LongTensor(neg_tails)

            # ----------------- 计算损失 -----------------
            pos_scores = model(heads, relations, tails)
            neg_scores = model(neg_heads, relations, neg_tails)
            loss = model.loss(pos_scores, neg_scores)

            # ----------------- 反向传播 -----------------
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        # ----------------- 模型保存与评估 -----------------
        avg_loss = total_loss / len(train_triplets)
        print(f"Epoch {epoch + 1}, Loss: {avg_loss:.4f}")

        if save_path and (epoch + 1) % 10 == 0:
            mrr, hits10 = evaluate(model, train_triplets[:10])  # 示例评估部分数据
            print(f"MRR: {mrr:.3f}, Hits@10: {hits10:.3f}")

            if mrr > best_mrr:
                best_mrr = mrr
                torch.save(model.state_dict(), save_path)
                print(f"Model saved at epoch {epoch + 1}")


def evaluate(model, test_triplets):
    model.eval()
    ranks = []
    hits_at_10 = 0

    with torch.no_grad():
        for h, r, t in test_triplets:
            # 生成所有可能的尾实体候选
            h_tensor = torch.LongTensor([h]).expand(model.num_entities)
            r_tensor = torch.LongTensor([r]).expand(model.num_entities)
            t_candidates = torch.arange(model.num_entities)

            # 计算所有候选得分
            scores = model(h_tensor, r_tensor, t_candidates)

            # 获取真实尾实体的排名（从0开始）
            sorted_indices = torch.argsort(scores)
            rank = (sorted_indices == t).nonzero().item() + 1
            ranks.append(1.0 / rank)

            if rank <= 10:
                hits_at_10 += 1

    mrr = np.mean(ranks)
    hits10 = hits_at_10 / len(test_triplets)
    return mrr, hits10


# 示例数据
if __name__ == "__main__":
    triplets = []
    with open('data/index_rel_triple.txt', 'r') as file:
        for line in file:
            head, relation, tail = line.strip().split('  ')
            triplets.append((int(head), int(relation), int(tail)))

    # 划分训练集/测试集
    train_data = triplets[:100]
    test_data = triplets[100:]

    # 初始化模型
    model = TransE(
        num_entities=168,
        num_relations=3,
        embedding_dim=200,
        margin=1.5,
        norm=True
    )

    # 训练并保存最佳模型
    train_transE(
        model,
        train_triplets=train_data,
        all_triplets=triplets,
        num_epochs=100,
        batch_size=32,
        lr=0.001,
        save_path="result/best_transe_model.pth"
    )

    # 加载最佳模型进行评估
    model.load_state_dict(torch.load("result/best_transe_model.pth"))
    mrr, hits10 = evaluate(model, test_data)
    print(f"\nFinal Evaluation - MRR: {mrr:.3f}, Hits@10: {hits10:.3f}")