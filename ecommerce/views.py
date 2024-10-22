from django.http import HttpResponse
from django.shortcuts import render

# def index(request):
#     return HttpResponse("Welcome to my eCommerce platform")


def index(request):
    # Any context data to pass to the template can be defined here
    context = {
        'message': 'Test line passed as context',
    }
    return render(request, 'ecommerce/index.html', context)
