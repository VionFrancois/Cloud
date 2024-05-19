from django.urls import path
from searchClient import views

urlpatterns = [
    path("", views.index, name='index'),
]