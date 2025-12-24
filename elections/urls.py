from django.urls import path
from . import views

app_name = 'elections'

urlpatterns = [
    path('', views.election_list, name='election_list'),
    path('<int:election_id>/', views.election_detail, name='election_detail'),
    path(
        '<int:election_id>/vote/<int:candidate_id>/',
        views.vote,
        name='vote'
    ),
    # 添加全局结果页面（不需要参数）
    path('results/', views.results, name='results'),
    # 单个选举结果页面（需要参数）
    path('<int:election_id>/results/', views.election_results, name='election_results'),
    # API 接口
    path('api/results/', views.api_results, name='api_results'),
]
