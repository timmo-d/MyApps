from django.urls import path
from . import views

app_name = 'datamgt'
urlpatterns = [
    #path('', views.DataMgtPageView.as_view(), name='index'),
    path('', views.create, name='index'),
]
