from django.db import models
from django.conf import settings
# Create your models here.

class NewCar(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=255)
    is_activated = models.BooleanField(default=False, verbose_name="نشان داده شود؟")

    year_of_manufacture = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    palet = models.CharField(max_length=40, blank=False)
    asnad = models.CharField(max_length=50, blank=False)
    color = models.CharField(max_length=20, blank=False)

    GEARBOX_CHOICES = [
        ('automatic', 'اتومات'),
        ('manual', 'گیر'),
    ]

    CURRENCY_CHOICES = [
        ('usd', 'دالر'),
        ('afn', 'افغانی'),
    ]

    currency = models.CharField(
        max_length=10,
        choices=CURRENCY_CHOICES,
        default='usd',
        verbose_name='واحد پول'
    )

    gearbox_type = models.CharField(max_length=20, choices=GEARBOX_CHOICES)

    fuel_type = models.CharField(max_length=200)

    MILEAGE_UNIT_CHOICES = [
        ('km', 'کیلومتر'),
        ('mile', 'مایل'),
    ]

    mileage_unit = models.CharField(
        max_length=10,
        choices=MILEAGE_UNIT_CHOICES,
        default='km',
        verbose_name='واحد کارکرد'
    )

    mileage_km = models.PositiveIntegerField(verbose_name='مقدار کارکرد')

    main_image = models.ImageField(upload_to='cars/', blank=True, null=True)
    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_mileage_display_text(self):
        unit = "کیلومتر" if self.mileage_unit == "km" else "مایل"
        return f"{self.mileage_km} {unit}"

    def get_price_display_text(self):
        currency = "دالر" if self.currency == "usd" else "افغانی"
        return f"{self.price} {currency}"
    
    def __str__(self):
        return f"{self.title} - {self.get_mileage_display_text()}"

    class Meta:
        verbose_name = "موتر های جدید"
        verbose_name_plural = "موتر های جدید"

        
    
class NewCarImage(models.Model):
    car = models.ForeignKey(NewCar, on_delete=models.CASCADE, related_name='images')
    
    image = models.ImageField(upload_to='cars/more_images/')
    
    caption = models.CharField(max_length=255, blank=True, null=True)
    
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.car.title} - تصویر اضافی"
    

class Wishlist(models.Model):
    user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE
)
    car = models.ForeignKey(NewCar, on_delete=models.CASCADE, related_name="wishlisted")
    is_active = models.BooleanField(default=True)  # 👈 مهم
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'car')

    def __str__(self):
        return f"{self.user.username} - {self.car.title}"