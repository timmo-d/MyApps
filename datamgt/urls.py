from django.urls import path
from . import views

app_name = 'datamgt'
urlpatterns = [
    path('', views.DataMgtPageView.as_view(), name='datamgt'),
    #path('', views.create, name='datamgt'),
]
