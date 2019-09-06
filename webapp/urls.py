from django.conf.urls import url
from . import views

urlpatterns = [
    #url(r'',include ('webapp.urls')),
    url(r'^register', views.register, name='register'),
    url(r'^login', views.login, name='login'),
    url(r'', views.register, name='register'),
]