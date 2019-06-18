from django.contrib import admin
from django.urls import path, include
from . import views
from django.shortcuts import render

# account:index
app_name = 'accounts'


# accounts/
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]

def login(request):
    if request.method == 'POST':
        # 로그인 로직 실행
        pass
    else: # GET /accounts/login/ -> html 페이지만 렌더링
        render(request, 'accounts/login.html')