from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('product/<int:pk>/', views.product, name='product'),
    path('search/', views.search, name='search'),
    path('category/<str:foo>', views.category, name='category'),

    ### Checkout routing paths
    path('checkout/', views.checkout, name='checkout'),
    path('process-order/', views.process_order, name='process_order'),
    path('orders/', views.order_history, name='order_history'),
    path('order-history/', views.order_history, name='order_history'),



]
