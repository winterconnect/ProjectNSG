from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = 'yyApp'
urlpatterns = [
    # path('', views.home),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('join/', views.choose_authority, name='join'),
    path('join/adopter/', views.join_adopter),
    path('join/guardian/', views.join_guardian),
    path('board/', views.BoardListView.as_view(), name='list'),
    path('writepost/', views.write_post),
    path('', views.home, name='index'),
    path('chart/', views.chart, name='chart'),
    path('postdetail/<int:postID>', views.post_detail, name='post_detail'),
    path('postdetail/delete', views.post_delete, name='post_delete'),

]
