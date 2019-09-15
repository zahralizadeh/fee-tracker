from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^price/', views.query_price, name='query_price'),

]