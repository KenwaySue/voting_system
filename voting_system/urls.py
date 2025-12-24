from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
from elections import views as election_views

urlpatterns = [
    path('', lambda request: redirect('elections:election_list'), name='home'),
    path('admin/', admin.site.urls),
    # 登录
    path('login/', auth_views.LoginView.as_view(template_name='elections/login.html'), name='login'),
    
    # 👇 退出
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    # 👇 注册 (新加的)
    path('register/', election_views.register, name='register'),
    
    # elections 应用路由
    path('elections/', include('elections.urls')),
]

