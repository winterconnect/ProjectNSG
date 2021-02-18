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
    path('board/', views.board_list, name='list'),
    path('search/', views.board_search, name='search'),    
    path('writepost/', views.write_post, name = 'write_post'),
    path('', views.home, name='index'),
    path('chart/', views.chart, name='chart'),
    path('postdetail/<int:postID>', views.post_detail, name='post_detail'),
    path('postdetail/delete', views.post_delete, name='post_delete'),    
    path('postdetail/<int:postID>/comment_write', views.comment_write, name='comment_write'),
    path('postdetail/<int:commentID>/comment_delete', views.comment_delete, name='comment_delete'),
    path('mypage/', views.mypage, name='mypage'),
    path('modifyadoption', views.modify_adoption, name='modify_adoption'),
    
]
