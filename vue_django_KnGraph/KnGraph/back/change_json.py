import json

from py2neo import Graph

from Users.models import SysUser

cate = {'章':0,'节':1,'知识点':2}
symbolSize = {'章':100,'节':70,'知识点':30}

def to_dict(rel):
    data = []
    links = []
    added_node = set()
    for r_line in rel:
        rels = r_line['rel'] if isinstance(r_line['rel'], list) else [r_line['rel']]
        for r in rels:
            source = r.start_node
            target = r.end_node
            name = type(r).__name__

            if source['name'] not in added_node:
                data_dict = {
                    'name': source['name'],
                    'category': cate[str(source.labels).replace(":", "")],
                    'symbolSize': symbolSize[str(source.labels).replace(":", "")],
                    'desc': source['desc'],
                }
                data.append(data_dict)
                added_node.add(source['name'])

            if target['name'] not in added_node:
                data_dict = {
                    'name': target['name'],
                    'category': cate[str(target.labels).replace(":", "")],
                    'symbolSize': symbolSize[str(target.labels).replace(":", "")],
                    'desc': target['desc'],
                }
                data.append(data_dict)
                added_node.add(target['name'])

            link_dict = {
                'source': source['name'],
                'target': target['name'],
                'name': name,
            }
            links.append(link_dict)


    neo4j_data = {
        'data':data,
        'links':links,
        'entity_dict': get_entity_dict()
    }

    neo4j_data_json = json.dumps(neo4j_data,ensure_ascii=False)
    print(type(neo4j_data_json))
    print("数据打包成功")

    return neo4j_data_json

def get_entity_dict():
    graph = Graph('bolt://localhost:7687', auth=('neo4j', 'zxz040312'))

    entity = graph.run("match (n) return n.name").data()
    rel = graph.run("MATCH (n1)- [rel] -> (n2) RETURN rel").data()

    dict_e = {}

    for idx, i in enumerate(entity):
        dict_e[i['n.name']] = False

    return dict_e