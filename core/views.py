from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
# Create your views here.

class HomePageView(TemplateView):
    template_name = "core/index.html"