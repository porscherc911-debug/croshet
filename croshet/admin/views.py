import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect, render

from .models import Product


DEFAULT_PRODUCTS = [
    {
        'name': 'Daisy Shoulder Bag',
        'price': 450,
        'category': 'Bags',
        'image_url': 'https://images.unsplash.com/photo-1594223274512-ad4803739b7c?auto=format&fit=crop&w=600&q=80',
        'description': 'A soft, stylish crochet shoulder bag.',
    },
    {
        'name': 'Flower Keychain',
        'price': 120,
        'category': 'Accessories',
        'image_url': 'https://images.unsplash.com/photo-1610701596007-11502861dcfa?auto=format&fit=crop&w=600&q=80',
        'description': 'A cute handmade crochet keychain.',
    },
    {
        'name': 'Rose Bouquet',
        'price': 250,
        'category': 'Flowers',
        'image_url': 'https://images.unsplash.com/photo-1561181286-d3fee7d55364?auto=format&fit=crop&w=600&q=80',
        'description': 'A long-lasting handmade crochet bouquet.',
    },
]


def ensure_default_products():
    if Product.objects.count() == 0:
        for item in DEFAULT_PRODUCTS:
            Product.objects.create(**item)


def products_api(request):
    ensure_default_products()

    if request.method == 'GET':
        products = Product.objects.all().order_by('id')
        payload = [
            {
                'id': product.id,
                'name': product.name,
                'price': float(product.price),
                'category': product.category,
                'img': product.image_url or 'https://images.unsplash.com/photo-1610701596007-11502861dcfa?auto=format&fit=crop&w=600&q=80',
                'description': product.description,
            }
            for product in products
        ]
        return JsonResponse({'products': payload})

    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8')) if request.body else {}
        except json.JSONDecodeError:
            data = {}

        action = data.get('action')
        product_id = data.get('id')

        if action == 'add':
            Product.objects.create(
                name=str(data.get('name', '')).strip() or 'New Product',
                price=data.get('price', 0) or 0,
                category=data.get('category', 'Accessories'),
                image_url=str(data.get('img', '') or data.get('image_url', '')).strip(),
                description=str(data.get('description', '')).strip(),
            )
        elif action == 'update' and product_id:
            product = Product.objects.filter(id=product_id).first()
            if product:
                product.name = str(data.get('name', product.name)).strip() or product.name
                product.price = data.get('price', product.price) or product.price
                product.category = data.get('category', product.category)
                product.image_url = str(data.get('img', product.image_url) or product.image_url).strip()
                product.description = str(data.get('description', product.description)).strip()
                product.save()
        elif action == 'delete' and product_id:
            Product.objects.filter(id=product_id).delete()
        else:
            return JsonResponse({'error': 'Unsupported action'}, status=400)

        return JsonResponse({'status': 'ok'})

    return JsonResponse({'error': 'Method not allowed'}, status=405)


def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_dashboard')

    error = None
    if request.method == 'POST':
        auth_action = request.POST.get('auth_action') or 'login'
        if auth_action == 'signup':
            return admin_signup(request)

        username = (request.POST.get('username') or '').strip()
        password = request.POST.get('password') or ''
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        error = 'Invalid admin username or password.'

    return render(request, 'admin/auth.html', {'mode': 'login', 'error': error})


def admin_signup(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_dashboard')

    error = None
    if request.method == 'POST':
        auth_action = request.POST.get('auth_action') or 'signup'
        if auth_action == 'login':
            return admin_login(request)

        username = (request.POST.get('username') or '').strip()
        password1 = request.POST.get('password1') or ''
        password2 = request.POST.get('password2') or ''

        if not username:
            error = 'Username is required.'
        elif password1 != password2:
            error = 'Passwords do not match.'
        elif len(password1) < 8:
            error = 'Password must be at least 8 characters long.'
        elif User.objects.filter(username=username).exists():
            error = 'This username is already taken.'
        else:
            user = User.objects.create_user(username=username, password=password1)
            user.is_staff = True
            user.is_superuser = True
            user.save()
            login(request, user)
            return redirect('admin_dashboard')

    return render(request, 'admin/auth.html', {'mode': 'signup', 'error': error})


def admin_logout(request):
    logout(request)
    return redirect('admin_login')


def admin_dashboard(request):
    if not request.user.is_staff:
        if request.method == 'POST' and request.POST.get('auth_action') in {'login', 'signup'}:
            if request.POST.get('auth_action') == 'login':
                return admin_login(request)
            return admin_signup(request)
        return render(request, 'admin/auth.html', {'mode': 'login', 'error': None})

    ensure_default_products()

    if request.method == 'POST':
        action = request.POST.get('action')
        product_id = request.POST.get('id')

        if action == 'add':
            Product.objects.create(
                name=request.POST.get('name', '').strip() or 'New Product',
                price=request.POST.get('price', 0) or 0,
                category=request.POST.get('category', 'Accessories'),
                image_url=request.POST.get('image_url', '').strip(),
                description=request.POST.get('description', '').strip(),
            )
        elif action == 'update' and product_id:
            product = Product.objects.filter(id=product_id).first()
            if product:
                product.name = request.POST.get('name', product.name).strip() or product.name
                product.price = request.POST.get('price', product.price) or product.price
                product.category = request.POST.get('category', product.category)
                product.image_url = request.POST.get('image_url', product.image_url).strip()
                product.description = request.POST.get('description', product.description).strip()
                product.save()
        elif action == 'delete' and product_id:
            Product.objects.filter(id=product_id).delete()

        return redirect('admin_dashboard')

    products = Product.objects.all()
    return render(request, 'admin/admin.html', {'products': products})
