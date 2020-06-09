from django.urls import path

from .views import HomePageView, AboutPageView, create, DataOutputView

urlpatterns = [
    path('about/', AboutPageView.as_view(), name='about'),
    path('', HomePageView.as_view(), name='home'),
    path('datamgt/', create, name='datamgt'),
    path('data-output/', DataOutputView.as_view(), name='data-output'),
]
