from django.urls import path
from . import views


urlpatterns = [
    path('', views.community, name='community'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
]