from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.BlackFlagListAPI.as_view(), name = 'blackflag-list'),
    path('post/', views.BlackFlagPostAPI.as_view(), name = 'blackflag-post'),
    path('check/', views.BlackFlagCheckAPI.as_view(), name = 'blackflag-check')
]