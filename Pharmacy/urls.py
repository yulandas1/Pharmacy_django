from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('pharmacy/', views.pharmacy, name='pharmacy'),
    path('employee/<int:employee_id>/', views.employee_details, name='employee_details'),
    path('customer/<int:customer_id>/orders/', views.customer_orders, name='customer_orders'),
    path('order/<int:order_id>/items/', views.order_items, name='order_items'),
    path('create-test-data/', views.create_test_data, name='create_test_data'),
]