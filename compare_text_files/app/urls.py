from django.urls import path
from . import views

urlpatterns = [
    path('',views.main,name='main'),
    # path('compare/',views.compare,name='compare')
]
