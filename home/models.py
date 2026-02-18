from django.db import models

# Create your models here.

class ContactUs(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True, verbose_name="عنوان")
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")

    location = models.CharField(max_length=255, verbose_name="موقعیت / آدرس")
    opening_hours = models.CharField(max_length=255, blank=True, null=True, verbose_name="ساعات کاری")

    phone_number = models.CharField(max_length=15, verbose_name="شماره تماس")
    phone_number_2 = models.CharField(max_length=15, blank=True, null=True, verbose_name="شماره تماس دوم")

    email = models.EmailField(blank=True, null=True, verbose_name="ایمیل")

    whatsapp = models.CharField(max_length=15, blank=True, null=True, verbose_name="واتساپ")
    telegram = models.CharField(max_length=100, blank=True, null=True, verbose_name="تلگرام")

    map_link = models.CharField(blank=True, null=True, verbose_name="لینک گوگل مپ", max_length=100000)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title if self.title else self.location
    

class AboutUs(models.Model):
    title = models.CharField(max_length=255, verbose_name="عنوان")  # Main title
    subtitle = models.CharField(max_length=255, blank=True, null=True, verbose_name="زیر عنوان")  # Optional subtitle
    experniance = models.FloatField(verbose_name="تجربه")
    description = models.TextField(verbose_name="توضیحات")  # Main content
    mission = models.TextField(blank=True, null=True, verbose_name="ماموریت")  # Optional mission statement
    vision = models.TextField(blank=True, null=True, verbose_name="چشم‌انداز")  # Optional vision statement
    values = models.TextField(blank=True, null=True, verbose_name="ارزش‌ها")  # Optional core values
    main_image = models.ImageField(upload_to="about_us/", blank=True, null=True, verbose_name="تصویر اصلی")  # Optional image
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    class Meta:
        verbose_name = "درباره ما"
        verbose_name_plural = "درباره ما"

    def __str__(self):
        return self.title
    

class CustomerMessage(models.Model):
    name = models.CharField(max_length=255, verbose_name="نام مشتری")
    email = models.EmailField(verbose_name="ایمیل")
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="شماره تماس")
    subject = models.CharField(max_length=255, verbose_name="موضوع")
    message = models.TextField(verbose_name="پیام")
    is_read = models.BooleanField(default=False, verbose_name="نمایش داده شود")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ارسال")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخرین بروزرسانی")

    class Meta:
        verbose_name = "پیام مشتری"
        verbose_name_plural = "پیام‌های مشتریان"
        ordering = ['-created_at']  # newest first

    def __str__(self):
        return f"{self.name} - {self.subject}"
    
class HeroSlider(models.Model):
    title = models.CharField(max_length=40)
    description = models.TextField()
    image = models.ImageField(upload_to="images/")
    is_read = models.BooleanField(default=False, verbose_name="نمایش داده شود")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ارسال")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخرین بروزرسانی")