from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('candidates/', views.candidate_list, name='candidate_list'),
    path('candidates/<int:candidate_id>/', views.candidate_detail, name='candidate_detail'),
    path('vote/', views.vote, name='vote'),
    path('results/', views.results, name='results'),
    path('api/results/', views.api_results, name='api_results'),
    path('login/', views.custom_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.custom_logout, name='logout'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
]