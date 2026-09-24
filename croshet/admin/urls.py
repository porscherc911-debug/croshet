from django.urls import path

from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('login/', views.admin_login, name='admin_login'),
    path('signup/', views.admin_signup, name='admin_signup'),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('api/products/', views.products_api, name='products_api'),
]
