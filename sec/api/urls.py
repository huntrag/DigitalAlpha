from django.urls import path
from . import views

urlpatterns = [ 
    path('', views.getAll),
    path('strict/',views.getStrict),
    path('<str:pk>/',views.getId),   
]