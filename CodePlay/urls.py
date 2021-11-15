from . import views
from django.urls import path, include
from django.contrib.staticfiles import views as vv

urlpatterns = [
    path('userinfo', views.userinfo),
    path('userScheme', views.userScheme),
    path('exploreScheme', views.exploreScheme),
    path('sketch', views.sketch),
]
