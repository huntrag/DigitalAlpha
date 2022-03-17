from django.urls import path
from . import views

urlpatterns = [ 
    path('', views.getAll),
    path('bs',views.getBS),
    path('strict',views.getStrict),
    path('<str:pk>',views.getId),    
]