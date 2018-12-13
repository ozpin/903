from django.urls import path
from . import  views
from django.conf.urls import url

urlpatterns = [
    url(r'', views.output,name = 'output'),
    # path('',views.eventsource,name = 'output'),
    # path('',views.output,name = 'output'),
]