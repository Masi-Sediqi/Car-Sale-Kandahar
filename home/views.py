from django.shortcuts import render, redirect
from products.models import *
from .models import *
from django.contrib import messages
# Create your views here.

def dashboard(request):
    cars = NewCar.objects.filter(is_activated=True).order_by('-created_at')[:4]
    hero_slider = HeroSlider.objects.filter(is_read=True)
    context = {
        'cars':cars,
        'hero_slider':hero_slider,
    }
    return render(request, 'dashboard.html', context)

def contact_us(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        subject = request.POST.get('msg_subject')
        message_text = request.POST.get('message')

        # Create the customer message record
        CustomerMessage.objects.create(
            name=name,
            email=email,
            phone_number=phone_number,
            subject=subject,
            message=message_text
        )

        messages.success(request, "پیام شما با موفقیت ارسال شد. با شما در تماس خواهیم بود.")
        return redirect('home:contact_us')  # refresh the page or redirect somewhere else

    # GET request
    return render(request, 'home/contact-us.html')

def about_us(request):
    about_us = AboutUs.objects.last()
    messages = CustomerMessage.objects.filter(is_read=True)
    return render(request, 'home/about-us.html', {'about_us':about_us, 'messages':messages})