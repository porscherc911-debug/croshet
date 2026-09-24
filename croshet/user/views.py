from django.shortcuts import render

from admin.models import Product


def home(request):
    products = Product.objects.all()
    return render(request, 'user/user.html', {'products': products})
