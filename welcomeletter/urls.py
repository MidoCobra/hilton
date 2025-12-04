from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('transfers/', views.transfers, name='transfers'),
    path('info/', views.info, name='info'),
    path('restaurants/', views.restaurants, name='restaurants'),
    path('kids/', views.kids, name='kids'),
    path('spa/', views.spa, name='spa'),
    path('board-menus/', views.board_menus, name='board_menus'),
    path('hilton-honors/', views.hilton_honors, name='hilton_honors'),
    path('subscribe/', views.subscribe_newsletter, name='subscribe_newsletter'),
]
