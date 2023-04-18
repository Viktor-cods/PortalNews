from django.contrib import admin
from django.urls import path,include
from .views import *


urlpatterns = [
    path('news_list/',index,name='index'),
    path('new/<str:slug>',default,name='default'),
    path('',Posts.as_view(),name='posts'),
    path('search/',PostSearch.as_view(),name='search'),
    path('create/',PostCreate.as_view(),name='create'),
    path('<int:pk>/update/',PostUpdate.as_view(),name='post_update'),
    path('<int:pk>/delete/',PostDelete.as_view(),name='post_delete'),
    path('subscriptions/',subscriptions,name='subscriptions'),
    path('categories/<int:pk>',CategoryListView.as_view(),name='category_list'),
    path('categories/<int:pk>/subscribe',subscribe,name='subscribe'),
]

