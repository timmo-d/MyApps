from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView
from django.urls import reverse

from .forms import Options
from .models import DataMgtOptions

from .src.controller import executeOptions


# Create your views here.
class HomePageView(TemplateView):
    template_name = 'home.html'


class AboutPageView(TemplateView):
    template_name = 'about.html'


class DataMgtPageView(TemplateView):
    template_name = 'datamgt.html'


class DataOutputView(TemplateView):
    template_name = 'data-output.html'

def create(response):
    if response.method == "POST":
        form = Options(response.POST)

        if form.is_valid():
            opt1 = form.cleaned_data['opt1']
            opt2 = form.cleaned_data['opt2']
            opt3 = form.cleaned_data['opt3']
            opt4 = form.cleaned_data['opt4']
            opt5 = form.cleaned_data['opt5']
            opt6 = form.cleaned_data['opt6']
            opt7 = form.cleaned_data['opt7']
            opt8 = form.cleaned_data['opt8']
            opt9 = form.cleaned_data['opt9']
            opt10 = form.cleaned_data['opt10']
            t = DataMgtOptions(opt1=opt1,opt2=opt2,opt3=opt3,opt4=opt4,opt5=opt5,opt6=opt6,opt7=opt7,opt8=opt8,opt9=opt9,opt10=opt10)
            t.save()
            executeOptions()
        return HttpResponseRedirect(reverse('data-output'))

    else:
        form = Options()
        # form = get_object_or_404(Options)

    return render(response, "datamgt.html", {"form":form})
