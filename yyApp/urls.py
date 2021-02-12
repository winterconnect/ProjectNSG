from django.urls import path
from . import views

app_name = 'yyApp'
urlpatterns = [
    path('join/', views.choose_authority),
    path('join/adopter/', views.join_adopter),
    path('join/guardian/', views.join_guardian),
    path('board/', views.BoardListView.as_view(), name='board_list'),
]
