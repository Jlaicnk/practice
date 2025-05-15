from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status

from KnGraph.back.graph_CRUD.neo4j_graph import NeoGraph
from Users.models import SysUser
from Users.serializers import SysuserPreferencesSerializer
from .back.change_json import to_dict
from .back.chat_bot import qa_robot
import json

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from KnGraph.back.KGE.recommend import Recommend


# Create your views here.

@api_view(['GET','POST'])
@authentication_classes([JWTAuthentication])  # 添加JWT身份认证
@permission_classes([IsAuthenticated])  # 添加权限校验
def search_relation(request):
	"""
	接收来自前端搜索表单（后续添加其他HTTP方式）
	:param request:
	:return:
	"""
	graph = NeoGraph()

	if request.method == 'GET':
		entity1 = request.GET['e1']
		relation = request.GET['rel']
		entity2 = request.GET['e2']
		min_l = request.GET['min']
		max_l = request.GET['max']
		limit = request.GET['limit']

	else:
		request.params = json.loads(request.body)
		entity1 = request.params['e1']
		relation = request.params['rel']
		entity2 = request.params['e2']
		min_l = request.params['min']
		max_l = request.params['max']
		limit = request.params['limit']


	if limit=="" : limit = 25
	if min_l=="" : min_l = 1
	if max_l=="" : max_l = 1

	query_methods = {
		(True, False, False): lambda: graph.find_by_e1(entity1, min_l=min_l, max_l=max_l, limit=limit),
		(False, False, True): lambda: graph.find_by_e2(entity2, min_l=min_l, max_l=max_l, limit=limit),
		(True, True, False): lambda: graph.find_by_e1_rel(entity1, relation, min_l=min_l, max_l=max_l, limit=limit),
		(False, True, True): lambda: graph.find_by_e2_rel(entity2, relation, min_l=min_l, max_l=max_l, limit=limit),
		(True, False, True): lambda: graph.find_by_e1_e2(entity1, entity2, min_l=min_l, max_l=10, limit=limit),
		(False, False, False): lambda: graph.find_all()
	}

	condition = (len(entity1) != 0, len(relation) != 0, len(entity2) != 0)

	# if condition in query_methods:
	# 	search_result = query_methods[condition]()
	# 	search_result = to_dict(search_result)
	# 	print(type(search_result))
	# 	return Response(data=search_result, status=status.HTTP_200_OK)
	# else:
	# 	return Response(data={"error": "Invalid input combination","message":"数据输入格式或后端生成数据错误"}, status=status.HTTP_400_BAD_REQUEST)
	# # 调用相应的方法
	if condition in query_methods:
		search_result = query_methods[condition]()
		print(type(search_result))
		if not search_result:
			return Response(data={"error": "No search results", "message": "无该实体或关系搜索结果"},
							status=status.HTTP_404_NOT_FOUND)
		search_result = to_dict(search_result)
		return Response(data=search_result, status=status.HTTP_200_OK)
	else:
		return Response(data={"error": "Invalid input combination", "message": "数据输入格式或后端生成数据错误"},
						status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET','POST'])
@authentication_classes([JWTAuthentication])  # 添加JWT身份认证
@permission_classes([IsAuthenticated])  # 添加权限校验
def AI_answer(request):
	if request.method == 'GET':
		question = request.GET['question']
	else:
		request.params = json.loads(request.body)
		question = request.params['question']
	try:
		dic = qa_robot(question)  # 假设qa_robot返回回答字符串
		return Response(data=dic, status=status.HTTP_200_OK)
	except Exception as e:
		return Response(data={"error": "Invalid input combination","message":"后端生成数据或数据返回错误"}, status=status.HTTP_400_BAD_REQUEST)

from .back.random import createRandom
@api_view(['POST'])
def getRandom(request):
	if request.method == 'POST':
		numNo = json.loads(request.body).get("numNo")
		numList = createRandom(numNo)
		return Response(numList, status=status.HTTP_200_OK)

@api_view(['POST'])
def UserRecommend(request):
	"""
    根据前端传来的 user_id，查询用户记录并返回用户的偏好信息。
    """
	try:
		# 解析前端传来的 JSON 数据
		data = json.loads(request.body)
		user_id = data['user_id']

	except (json.JSONDecodeError, KeyError):
		# 如果 JSON 格式错误或缺少必要字段，返回错误响应
		return Response({"error": "请求数据格式错误"}, status=status.HTTP_400_BAD_REQUEST)

	try:
		# 根据 user_id 查询用户记录
		user = SysUser.objects.get(id=user_id)

	except ObjectDoesNotExist:
		# 如果用户不存在，返回用户不存在的错误响应
		return Response({"error": "用户不存在"}, status=status.HTTP_404_NOT_FOUND)

	preferences = user.preferences
	re = Recommend()
	recommend_items = re.get_recommend_item(preferences, 10)

	return Response({"recommendItems": recommend_items}, status=status.HTTP_200_OK)







