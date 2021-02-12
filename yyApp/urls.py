from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'yyApp'
urlpatterns = [
    # path('', views.home),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('join/', views.choose_authority, name='join'),
    path('join/adopter/', views.join_adopter),
    path('join/guardian/', views.join_guardian),
    path('writepost/', views.write_post),
    path('postdetail/', views.post_detail),
    # path('postlike/', views.post_like, name='post_like'),
    path('board/', views.BoardListView.as_view(), name='board_list'),
    path('', views.home, name='index'),
    path('pie-chart/', views.pie_chart, name='pie-chart'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
