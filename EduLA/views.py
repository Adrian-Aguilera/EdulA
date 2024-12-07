from django.shortcuts import render

def index(request):
  return render(request, 'index.html')

def error_504(request, exception=None):
    return render(request, '504.html', status=504)

def error_404(request, exception=None):
    return render(request, '404.html', status=404)