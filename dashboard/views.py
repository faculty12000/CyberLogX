from django.shortcuts import render
from django.http import HttpResponse

def home(request):
	return HttpResponse("<h1>Welcome to CyberLogX Threat Detection Dashboard</h1>")

# Create your views here.
