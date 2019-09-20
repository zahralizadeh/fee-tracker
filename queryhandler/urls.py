from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^price', views.query_price, name='query_price'),
    url(r'^whatisprice', views.whatisprice, name='whatisprice'),

]