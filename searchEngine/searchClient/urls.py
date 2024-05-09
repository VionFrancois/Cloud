from django.urls import path
from searchClient import views

urlpatterns = [
    path("index/", views.index, name='index'),
]