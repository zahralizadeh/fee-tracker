from django.conf.urls import url
from . import views

urlpatterns = [
    #url(r'',include ('webapp.urls')),
    url(r'^register/', views.register, name='register'),
    url(r'', views.register, name='register'),
]