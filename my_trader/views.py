from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.
# class AboutPageView(TemplateView):
#     template_name = 'pages/about.html'


class HomePageView(TemplateView):
    template_name = 'home.html'


