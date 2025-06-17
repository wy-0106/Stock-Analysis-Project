from django.urls import path
from . import views

urlpatterns = [

    path('main', views.project_tmx_money_analysis_main, name='project-tmx-money-analysis-main'),
    path('symbol/<str:symbol>/', views.stock_detail, name='stock-detail'),

]