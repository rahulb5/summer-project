from django.urls import path
from . import views


app_name = 'deploy'

urlpatterns = [
        path("deploy/", views.deploy , name = "deploy" ),
        path("truncate/", views.truncate, name = "truncate")
]

