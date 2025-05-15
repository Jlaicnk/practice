from django.urls import path
from . import views

urlpatterns = [
    path('search_relation/', views.search_relation, name='search_relation'), #关系查询
    path('AI_answer/', views.AI_answer, name='AI_answer'),#AI问答
    path('recommend/', views.UserRecommend, name='recommend'),#用户推荐
    path('getRandom/',views.getRandom,name='getRandom'),
]

