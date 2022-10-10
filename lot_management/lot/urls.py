from django.urls import path
from . import views

app_name = 'lot'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'), # 空文字の場合スラッシュをつけない
    #path('stream/', views.stream_view(), name='stream'), # ローカルwebcamをopencvで使う場合
    path('product/', views.ProductView.as_view(), name='product'),
    path('stock/', views.StockView.as_view(), name='stock'),
    path('edit/', views.EditView.as_view(), name='edit'),
    path('download/', views.DownloadView.as_view(), name='download'),
    path('print/', views.PrintView.as_view(), name='print'), 
    path('mypage/', views.MyPageView.as_view(), name='mypage'),
]