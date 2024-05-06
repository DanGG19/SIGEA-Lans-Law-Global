from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'SIGEA_APP/index.html')

def login(request):
    return render(request, 'SIGEA_APP/login.html')





