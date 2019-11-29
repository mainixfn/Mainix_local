from django.shortcuts import render
from django.http import  HttpResponse
from django.conf import settings

def main(request):
    return render(request, 'index.html')

def error404(request):
    return render(request, "404.html", status=404)



# Create your views here.
