from django.urls import path
from searchClient import views as searchViews
from users import views as users_views

urlpatterns = [
    path("index/", searchViews.index_view, name='search_index'),
    path('logout/', users_views.logout_view, name='logout'),
]