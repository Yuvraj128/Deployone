from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name="index"),
    path('getAuth/',views.oauth_response,name='oauth-response'),
    path('get-metadata/',views.getMetaData,name='getmetadata'),
]
