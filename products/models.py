from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class NewCar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    is_activated = models.BooleanField(default=False)
    
    year_of_manufacture = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    
    GEARBOX_CHOICES = [
        ('automatic', 'اتومات'),
        ('manual', 'گیر'),
    ]
    gearbox_type = models.CharField(max_length=20, choices=GEARBOX_CHOICES)
    
    FUEL_CHOICES = [
        ('petrol', 'پترول'),
        ('diesel', 'ډیزل'),
        ('electric', 'گازی'),
        ('hybrid', 'هایبرید'),
    ]
    fuel_type = models.CharField(max_length=20, choices=FUEL_CHOICES)
    
    mileage_km = models.PositiveIntegerField(verbose_name='کارکرد (کیلومتر)')    
    main_image = models.ImageField(upload_to='cars/', blank=True, null=True)

    description = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.mileage_km}"
    
class NewCarImage(models.Model):
    car = models.ForeignKey(NewCar, on_delete=models.CASCADE, related_name='images')
    
    image = models.ImageField(upload_to='cars/more_images/')
    
    caption = models.CharField(max_length=255, blank=True, null=True)
    
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.car.title} - تصویر اضافی"