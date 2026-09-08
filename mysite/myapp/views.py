from django.http import HttpResponse

def home(request):
    """Главная страница"""
    return HttpResponse("Hello, Django!")
