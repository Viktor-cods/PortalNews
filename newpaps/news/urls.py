from django.contrib import admin
from django.urls import path,include
from .views import (PostList,PostDetail,PostCreate,PostSearch,PostDelete,PostUpdate,index,default)


urlpatterns = [
    path('news_list/',index,name='index'),
    path('new/<str:slug>',default,name='default'),
    path('',PostList.as_view(), name='post'),
    path('news/search/',PostSearch.as_view(),name='search'),
    path('news/create/', PostCreate.as_view(), name='create'),
    path('news/<int:pk>/update/',PostUpdate.as_view(),name='post_update'),
    path('news/<int:pk>/delete/',PostDelete.as_view(),name='post_delete'),
]

