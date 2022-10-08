from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'), # https://ホスト/signup/ アクセス時
    path('signup_success/', views.SignUpSuccessView.as_view(), name='signup_success'), # https://ホスト/signup_success/
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'), # https://ホスト/login/ 
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'), # https://ホスト/logout/ 
    path('mypage/', views.MyPageView.as_view(), name='mypage'),
]