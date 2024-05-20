from django.urls import path
from searchClient import views
from users import views as users_views

urlpatterns = [
    path("index/", views.index, name='index'),
    path('logout/', users_views.logout_view, name='logout'),
]