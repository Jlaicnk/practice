from django.contrib.auth import authenticate, login, logout
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer, SysuserPreferencesSerializer
from .models import SysUser
from django.contrib.auth.hashers import make_password
import json
class RegisterView(generics.CreateAPIView):
    queryset = SysUser.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        data = {
            'user': {
                'username': user.username,
                'email': user.email,
                'phonenumber': user.phonenumber,
                'avatar': user.avatar.url if user.avatar else None
            },
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return Response(data, status=status.HTTP_201_CREATED)

class LoginView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        data = {
            'user': {
                'username': user.username,
                'email': user.email,
                'phonenumber': user.phonenumber,
                'avatar': user.avatar.url if user.avatar else None
            },
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return Response(data, status=status.HTTP_200_OK)

class LogoutView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_205_RESET_CONTENT)

class UserPreferencesView(APIView):
    permission_classes = []

    def post(self, request):
        user_id = request.data["user_id"]
        print("QWQSD:",request.user.id)
        try:
            user = SysUser.objects.get(id=user_id)
            # if user != request.user:
            #     return Response({"error": "无权限访问用户的数据"}, status=status.HTTP_403_FORBIDDEN)
            serializer = SysuserPreferencesSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except SysUser.DoesNotExist:
            return Response({"error": "用户不存在"}, status=status.HTTP_404_NOT_FOUND)

from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from Users.models import SysUser
from .serializers import SysuserPreferencesSerializer

@api_view(['POST'])
@csrf_exempt  # 如果需要禁用 CSRF（对于跨域请求），可以根据需要启用此装饰器
def alterUserPreferences(request):
    # 解析前端传来的 JSON 数据
    try:
        data = json.loads(request.body)
        user_id = data['user_id']
        preferences = data['preferences']
    except (json.JSONDecodeError, KeyError):
        return JsonResponse({"error": "请求数据格式错误"}, status=status.HTTP_400_BAD_REQUEST)

    # 根据 user_id 查找用户记录
    try:
        user = SysUser.objects.get(id=user_id)
    except ObjectDoesNotExist:
        return JsonResponse({"error": "用户不存在"}, status=status.HTTP_404_NOT_FOUND)

    # 更新用户的 preferences 字段
    user.preferences = preferences
    user.save()

    # 返回更新后的用户偏好信息
    serializer = SysuserPreferencesSerializer(user)
    return JsonResponse(serializer.data, status=status.HTTP_200_OK)


    # def post(self, request):
    #     user_id = request.user.id
    #     try:
    #         user = SysUser.objects.get(id=user_id)
    #         if user != request.user:
    #             return Response({"error": "无权限访问该用户的数据"}, status=status.HTTP_403_FORBIDDEN)
    #         node = request.data.get('node')
    #         isfavourite = request.data.get('isfavourite')
    #
    #         if not node:
    #             return Response({"error": "节点信息缺失"}, status=status.HTTP_400_BAD_REQUEST)
    #
    #         preferences = user.preferences
    #
    #         if isfavourite == 1 and node not in preferences:
    #             preferences.append(node)
    #         elif isfavourite == 0 and node in preferences:
    #             preferences.remove(node)
    #
    #         user.preferences = preferences
    #         user.save()
    #         serializer = SysuserPreferencesSerializer(user)
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     except SysUser.DoesNotExist:
    #         return Response({"error": "用户不存在"}, status=status.HTTP_404_NOT_FOUND)
    #     except Exception as e:
    #         return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)