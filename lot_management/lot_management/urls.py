"""lot_management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls), 
    path('lot/', include('lot.urls')), # LOTアプリ
    path('accounts/', include('allauth.urls')), # allauth（これを使用する場合は以下のデフォルト認証システムは不要） 
    #path('', include('accounts.urls')), # ユーザ認証まわり
    # path('password_change/', auth_views.PasswordChangeView.as_view( # パスワード変更
    #     template_name='accounts/password_change_form.html'), name='password_change'),
    # path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(
    #     template_name='accounts/password_change_done.html'), name='password_change_done'),
    # path('password_reset/', auth_views.PasswordResetView.as_view( # DBに登録済みメールアドレスに1回限り有効なリンクを作成（されていない場合は送信されない）
    #     template_name='accounts/password_reset.html'), name='password_reset'), # パスワードリセット申請ページ
    # path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
    #     template_name='accounts/password_reset_sent.html'), name='password_reset_done'), # メール送信完了ページ
    # path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view( # PasswordResetConfirmView: プロジェクト直下のurl設定を参照
    #     template_name='accounts/password_reset_form.html'), name='password_reset_confirm'), # パスワードリセットフォームページ
    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
    #     template_name='accounts/password_reset_done.html'), name='password_reset_complete'), # パスワードリセット完了ページ
]
