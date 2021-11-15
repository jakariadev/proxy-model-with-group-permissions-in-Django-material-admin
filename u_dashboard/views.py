from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import HttpResponse


class DashboardView(TemplateView):
    template_name = 'u_dashboard/dashboard.html'
