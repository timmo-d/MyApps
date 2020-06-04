from django.urls import path

from .views import HomePageView, AboutPageView, AnalysisPageView

urlpatterns = [
    path('about/', AboutPageView.as_view(), name='about'),
    path('', HomePageView.as_view(), name='home'),
    path('analysis/', AnalysisPageView.as_view(), name='analysis'),
]
