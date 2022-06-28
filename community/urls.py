from django.urls import path
from . import views


urlpatterns = [
    path('', views.community, name='community'),
    path('add_post/', views.add_post, name="add_post"),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
]