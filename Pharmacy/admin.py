from django.contrib import admin
from .models import (
    Employee, Salary, Suppliers, Customers, 
    Medicines, Orders, OrderedMedicines, Supplies
)

# Регистрируем все модели
# admin.site.register(Employee)
# admin.site.register(Salary)
# admin.site.register(Suppliers)
# admin.site.register(Customers)
# admin.site.register(Medicines)
# admin.site.register(Orders)
# admin.site.register(OrderedMedicines)
# admin.site.register(Supplies)

# Можно добавить кастомные админ-классы для удобства
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'age', 'phone', 'email')
    search_fields = ('first_name', 'last_name', 'email')

@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'order_date', 'order_status', 'total_amount')
    list_filter = ('order_status', 'order_date')
    search_fields = ('customer__first_name', 'customer__last_name')