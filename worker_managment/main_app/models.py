from django.db import models

class Worker(models.Model):
    name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    cnic = models.CharField(max_length=15, unique=True)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    gross_salary = models.DecimalField(max_digits=10, decimal_places=2)
    date_of_joining = models.DateField()
    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='worker_photos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class SalaryIncrement(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name='increments')
    year = models.IntegerField()
    increment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.worker.name} - {self.year}: PKR {self.increment_amount}"
