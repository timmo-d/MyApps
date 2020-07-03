from django.urls import path

from . import views

app_name = 'sentiment'
urlpatterns = [
    path('', views.SentimentPageView.as_view(), name='sentiment'),
]