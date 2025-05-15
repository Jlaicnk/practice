import pandas as pd
import json
dict = {}
list1 = []
list2 = []
with open('data\\chapter.json',encoding='UTF-8') as f:
    n1 = json.loads(f.read())
with open('data\\section.json',encoding='UTF-8') as f:
    n2 = json.loads(f.read())
data = pd.read_excel('data\\关系.xlsx')
for i,v in data.iterrows():
    dict[v[0]]=0
    dict[v[1]]=0

for i in dict:
    list1.append(i)

for i in list1:
    if i not in n1:
        if i not in n2:

            list2.append(i)
print(list2)
with open('data\\point.json','w',encoding='UTF-8') as f:
    json.dump(list2,f)


"""


"""