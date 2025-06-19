from django.shortcuts import render, redirect
from .models import LogFile

def home(request):
	# return HttpResponse("<h1>Welcome to CyberLogX Threat Detection Dashboard</h1>")
	if request.method == 'POST' and request.FILES.get('logfile'):
		LogFile.objects.create(file=request.FILES['logfile'])
		return redirect('home')
	logs = LogFile.objects.order_by('-uploaded_at')
	return render(request, 'dashboard/dashboard.html', {'logs': logs})

# Create your views here.
