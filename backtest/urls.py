from django.urls import path
from . import views

app_name = "backtest"

urlpatterns = [
    path('get_data/' , views.get_data, name= "get_data"),
    path('get_data/submit/', views.submit , name = "submit"),
    path('get_data/details/', views.details , name = "details"),
    path('deployed', views.deploy_strategy, name = "deployed"),
]