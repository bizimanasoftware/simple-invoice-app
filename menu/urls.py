from django.urls import path
from . import views

app_name = 'menu'
urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.dashboard_view, name='dashboard'),
    path('generate-receipt/', views.generate_receipt_view, name='generate_receipt'),
    path('delete-product/<int:product_id>/', views.delete_product_view, name='delete_product'),
    path('get-products-for-receipt/', views.get_products_for_receipt, name='get_products_for_receipt'),
    path('delete-product/<int:product_id>/', views.delete_product_view, name='delete_product'),

]
