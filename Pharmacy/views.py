from django.shortcuts import render
from django.http import HttpResponse
from .models import (
    Employee, Salary, Suppliers, Customers, 
    Medicines, Orders, OrderedMedicines, Supplies
)

def index(request):
    return render(request, 'pharmacy.html')

def pharmacy(request):
    # Используем first() вместо get() и проверяем существование объектов
    
    # 1. Получить первого сотрудника (если существует)
    employee = Employee.objects.first()
    
    # 2. Получить первого клиента (если существует)
    customer = Customers.objects.first()
    
    # 3. Получить первый заказ (если существует)
    order = Orders.objects.first()
    
    # 4. Получить первое лекарство (если существует)
    medicine = Medicines.objects.first()
    
    # 5. Получить первого поставщика (если существует)
    supplier = Suppliers.objects.first()
    
    # Получаем данные только если объекты существуют
    salaries = employee.salaries.all() if employee else []
    orders = customer.orders.all() if customer else []
    ordered_medicines = order.ordered_medicines.all() if order else []
    supplies = medicine.supplies.all() if medicine else []
    supplier_supplies = supplier.supplies.all() if supplier else []
    
    # Получаем другие данные с проверками
    order_total = order.total_amount if order else 0
    
    # Получаем сотрудника из зарплаты (если есть зарплаты)
    salary = Salary.objects.first()
    salary_employee = salary.employee if salary else None
    
    context = {
        'employee': employee,
        'customer': customer,
        'order': order,
        'medicine': medicine,
        'supplier': supplier,
        'salaries': salaries,
        'orders': orders,
        'ordered_medicines': ordered_medicines,
        'supplies': supplies,
        'supplier_supplies': supplier_supplies,
        'order_total': order_total,
        'salary_employee': salary_employee,
        'order_customer': order.customer if order else None,
    }
    
    return render(request, 'pharmacy.html', context)

def employee_details(request, employee_id):
    """Пример: получить сотрудника и все его зарплаты"""
    try:
        employee = Employee.objects.get(id=employee_id)
        salaries = employee.salaries.all().order_by('-effective_date')
        
        context = {
            'employee': employee,
            'salaries': salaries,
        }
        return render(request, 'employee_details.html', context)
    except Employee.DoesNotExist:
        return HttpResponse(f"Сотрудник с ID {employee_id} не найден.")
    except Exception as e:
        return HttpResponse(f"Ошибка: {e}")

def customer_orders(request, customer_id):
    """Пример: получить клиента и все его заказы"""
    try:
        customer = Customers.objects.get(id=customer_id)
        orders = customer.orders.all().order_by('-order_date')
        
        context = {
            'customer': customer,
            'orders': orders,
        }
        return render(request, 'customer_orders.html', context)
    except Customers.DoesNotExist:
        return HttpResponse(f"Клиент с ID {customer_id} не найден.")
    except Exception as e:
        return HttpResponse(f"Ошибка: {e}")

def order_items(request, order_id):
    """Пример: получить заказ и все лекарства в нём"""
    try:
        order = Orders.objects.get(id=order_id)
        ordered_items = order.ordered_medicines.all()
        
        context = {
            'order': order,
            'ordered_items': ordered_items,
            'total_amount': order.total_amount if order else 0,
        }
        return render(request, 'order_items.html', context)
    except Orders.DoesNotExist:
        return HttpResponse(f"Заказ с ID {order_id} не найден.")
    except Exception as e:
        return HttpResponse(f"Ошибка: {e}")

# Новая функция для создания тестовых данных
def create_test_data(request):
    """Создание тестовых данных для демонстрации связей"""
    try:
        # 1. Создаем сотрудника
        employee = Employee.objects.create(
            first_name="Иван",
            last_name="Петров",
            age=30,
            phone="+79991234567",
            email="ivan@example.com"
        )
        
        # 2. Создаем зарплату для сотрудника
        Salary.objects.create(
            employee=employee,
            amount=50000.00,
            effective_date="2024-01-01"
        )
        
        # 3. Создаем клиента
        customer = Customers.objects.create(
            first_name="Анна",
            last_name="Сидорова",
            age=25,
            phone="+79997654321",
            email="anna@example.com"
        )
        
        # 4. Создаем лекарство
        medicine = Medicines.objects.create(
            name="Парацетамол",
            price=150.50,
            stock_quantity=100
        )
        
        # 5. Создаем поставщика
        supplier = Suppliers.objects.create(
            first_name="Олег",
            last_name="Поставщиков",
            phone="+79998887766",
            email="supplier@example.com"
        )
        
        # 6. Создаем заказ
        order = Orders.objects.create(
            customer=customer,
            order_status="completed"
        )
        
        # 7. Добавляем лекарство в заказ
        OrderedMedicines.objects.create(
            order=order,
            medicine=medicine,
            quantity=2
        )
        
        # 8. Создаем поставку
        Supplies.objects.create(
            medicine=medicine,
            supplier=supplier,
            supply_date="2024-01-15",
            quantity=50
        )
        
        return HttpResponse('''
            <h1>Тестовые данные созданы!</h1>
            <p>Были созданы:</p>
            <ul>
                <li>Сотрудник: Иван Петров</li>
                <li>Клиент: Анна Сидорова</li>
                <li>Лекарство: Парацетамол</li>
                <li>Поставщик: Олег Поставщиков</li>
                <li>Заказ с лекарствами</li>
                <li>Зарплата сотрудника</li>
                <li>Поставка лекарства</li>
            </ul>
            <a href="/">Вернуться на главную</a>
        ''')
        
    except Exception as e:
        return HttpResponse(f"Ошибка при создании данных: {e}") 
def order_items(request, order_id):
    """Пример: получить заказ и все лекарства в нём"""
    try:
        order = Orders.objects.get(id=order_id)
        ordered_items = order.ordered_medicines.all()
        
        context = {
            'order': order,
            'ordered_items': ordered_items,
            'total_amount': order.total_amount if order else 0,
        }
        return render(request, 'order_items.html', context)
    except Orders.DoesNotExist:
        return HttpResponse(f"Заказ с ID {order_id} не найден.")
    except Exception as e:
        return HttpResponse(f"Ошибка: {e}")
    

def create_test_data(request):
    """Создание тестовых данных для демонстрации связей"""
    try:
        # Проверяем, существует ли уже тестовый сотрудник
        employee, employee_created = Employee.objects.get_or_create(
            email="ivan@example.com",
            defaults={
                'first_name': "Иван",
                'last_name': "Петров",
                'age': 30,
                'phone': "+79991234567",
            }
        )
        
        if employee_created:
            # Создаем зарплату для сотрудника только если он был создан
            Salary.objects.get_or_create(
                employee=employee,
                amount=50000.00,
                effective_date="2024-01-01"
            )
        
        # Проверяем, существует ли уже тестовый клиент
        customer, customer_created = Customers.objects.get_or_create(
            email="anna@example.com",
            defaults={
                'first_name': "Анна",
                'last_name': "Сидорова",
                'age': 25,
                'phone': "+79997654321",
            }
        )
        
        # Проверяем, существует ли уже тестовое лекарство
        medicine, medicine_created = Medicines.objects.get_or_create(
            name="Парацетамол",
            defaults={
                'price': 150.50,
                'stock_quantity': 100
            }
        )
        
        # Проверяем, существует ли уже тестовый поставщик
        supplier, supplier_created = Suppliers.objects.get_or_create(
            email="supplier@example.com",
            defaults={
                'first_name': "Олег",
                'last_name': "Поставщиков",
                'phone': "+79998887766",
            }
        )
        
        # Создаем заказ, если нет заказов у клиента
        order, order_created = Orders.objects.get_or_create(
            customer=customer,
            order_status="completed"
        )
        
        # Добавляем лекарство в заказ, если его еще нет
        if order_created:
            OrderedMedicines.objects.get_or_create(
                order=order,
                medicine=medicine,
                defaults={'quantity': 2}
            )
        
        # Создаем поставку, если ее еще нет
        Supplies.objects.get_or_create(
            medicine=medicine,
            supplier=supplier,
            supply_date="2024-01-15",
            defaults={'quantity': 50}
        )
        
        # Подсчитываем созданные объекты
        created_count = 0
        if employee_created:
            created_count += 1
        if customer_created:
            created_count += 1
        if medicine_created:
            created_count += 1
        if supplier_created:
            created_count += 1
        
        return HttpResponse(f'''
            <h1>Тестовые данные {'созданы' if created_count > 0 else 'уже существуют'}!</h1>
            <p>Статус создания:</p>
            <ul>
                <li>Сотрудник: Иван Петров - {'создан' if employee_created else 'уже существует'}</li>
                <li>Клиент: Анна Сидорова - {'создан' if customer_created else 'уже существует'}</li>
                <li>Лекарство: Парацетамол - {'создано' if medicine_created else 'уже существует'}</li>
                <li>Поставщик: Олег Поставщиков - {'создан' if supplier_created else 'уже существует'}</li>
            </ul>
            <p>Всего создано объектов: {created_count}</p>
            <a href="/">Вернуться на главную</a>
        ''')
        
    except Exception as e:
        return HttpResponse(f"Ошибка при создании данных: {e}<br><a href='/'>Вернуться на главную</a>")
    
# from django.shortcuts import render
# from django.http import HttpResponse

# def index(request):
#     return HttpResponse('Добро пожаловать на главную страницу')

# def pharmacy(request):
#     # Временно закомментируем код, использующий базу данных
#     # или обрабатываем возможное исключение
    
#     try:
#         # Примеры использования связей
#         from .models import Employee, Customers, Orders
        
#         # 1. Получить все зарплаты сотрудника
#         employee = Employee.objects.first()
        
#         # 2. Получить все заказы клиента
#         customer = Customers.objects.first()
        
#         # 3. Получить все лекарства в заказе
#         order = Orders.objects.first()
        
#         context = {
#             'employee': employee,
#             'customer': customer,
#             'order': order,
#         }
        
#         return render(request, 'pharmacy.html', context)
        
#     except Exception as e:
#         # Если таблицы еще не созданы, покажем простую страницу
#         return HttpResponse(f'''
#             <h1>Приветствуем в Pharmacy System!</h1>
#             <p>База данных еще не настроена.</p>
#             <p>Выполните в терминале:</p>
#             <pre>
# python manage.py makemigrations
# python manage.py migrate
#             </pre>
#             <p>Ошибка: {e}</p>
#         ''')

# def employee_details(request, employee_id):
#     """Пример: получить сотрудника и все его зарплаты"""
#     try:
#         employee = Employee.objects.get(id=employee_id)
#         salaries = employee.salaries.all().order_by('-effective_date')
        
#         context = {
#             'employee': employee,
#             'salaries': salaries,
#         }
#         return render(request, 'employee_details.html', context)
#     except:
#         return HttpResponse("Данные еще не готовы. Выполните миграции.")

# def customer_orders(request, customer_id):
#     """Пример: получить клиента и все его заказы"""
#     try:
#         customer = Customers.objects.get(id=customer_id)
#         orders = customer.orders.all().order_by('-order_date')
        
#         context = {
#             'customer': customer,
#             'orders': orders,
#         }
#         return render(request, 'customer_orders.html', context)
#     except:
#         return HttpResponse("Данные еще не готовы. Выполните миграции.")

# def order_items(request, order_id):
#     """Пример: получить заказ и все лекарства в нём"""
#     try:
#         order = Orders.objects.get(id=order_id)
#         ordered_items = order.ordered_medicines.all()
        
#         context = {
#             'order': order,
#             'ordered_items': ordered_items,
#             'total_amount': order.total_amount,
#         }
#         return render(request, 'order_items.html', context)
#     except:
#         return HttpResponse("Данные еще не готовы. Выполните миграции.")