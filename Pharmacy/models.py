from django.db import models
from django.core.validators import MinValueValidator
from datetime import date

class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField(validators=[MinValueValidator(18)])
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
        
    class Meta:
        db_table = 'employee'

class Salary(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='salaries')
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    effective_date = models.DateField(default=date.today)

    def __str__(self):
        return f"{self.employee}: {self.amount}"
        
    class Meta:
        db_table = 'salary'
        verbose_name_plural = 'salaries'

class Suppliers(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
        
    class Meta:
        db_table = 'suppliers'
        verbose_name_plural = 'suppliers'

class Customers(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField(validators=[MinValueValidator(0)])
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
        
    class Meta:
        db_table = 'customers'

class Medicines(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    stock_quantity = models.IntegerField(validators=[MinValueValidator(0)])
    
    def __str__(self):
        return self.name
        
    @property
    def is_expired(self):
            return self.expiration_date < date.today()
        
    class Meta:
        db_table = 'medicines'
        verbose_name_plural = 'medicines'

class Orders(models.Model):
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE, related_name='orders')
    order_date = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    
    def __str__(self):
        return f"Order #{self.id} - {self.customer}"
        
    @property
    def total_amount(self):
        return sum(item.total_price for item in self.ordered_medicines.all())
        
    class Meta:
        db_table = 'orders'
        verbose_name_plural = 'orders'

class OrderedMedicines(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name='ordered_medicines')
    medicine = models.ForeignKey(Medicines, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    
    def __str__(self):
        return f"{self.medicine.name} x{self.quantity}"
        
    @property
    def total_price(self):
        return self.medicine.price * self.quantity
        
    class Meta:
        db_table = 'ordered_medicines'
        verbose_name_plural = 'ordered_medicines'
        unique_together = ['order', 'medicine']

class Supplies(models.Model):
    medicine = models.ForeignKey(Medicines, on_delete=models.CASCADE, related_name='supplies')
    supplier = models.ForeignKey(Suppliers, on_delete=models.CASCADE, related_name='supplies')
    supply_date = models.DateField(default=date.today)
    quantity = models.IntegerField(validators=[MinValueValidator(1)], default=1)
    
    def __str__(self):
        return f"{self.medicine} from {self.supplier}"
        
    class Meta:
            db_table = 'supplies'
            verbose_name_plural = 'supplies'