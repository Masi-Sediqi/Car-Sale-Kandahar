from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
# Create your views here.

def add_listing(request):
    if not request.user.is_authenticated:
        return redirect('account_login')

    if not request.user.emailaddress_set.filter(verified=True).exists():
        return redirect('account_email_verification_sent')
    
    if request.method == 'POST':
        # Get main car fields
        title = request.POST.get('title')
        brand_model = request.POST.get('brand_model')
        price = request.POST.get('price')
        year_of_manufacture = request.POST.get('year_of_manufacture')
        gearbox_type = request.POST.get('gearbox_type')
        fuel_type = request.POST.get('fuel_type')
        mileage_km = request.POST.get('mileage_km')
        description = request.POST.get('description')
        main_image = request.FILES.get('main_image')  # optional main image

        # Create the main NewCar record
        car = NewCar.objects.create(
            title=title,
            brand_model=brand_model,
            price=price,
            year_of_manufacture=year_of_manufacture,
            gearbox_type=gearbox_type,
            fuel_type=fuel_type,
            mileage_km=mileage_km,
            main_image=main_image,
            description=description,
        )

        # Handle multiple images with captions
        for key in request.FILES:
            if key.startswith('more_images_'):
                # Get index from input name: e.g., more_images_0
                index = key.split('_')[-1]
                image_file = request.FILES[key]
                caption = request.POST.get(f'image_caption_{index}', '')
                NewCarImage.objects.create(
                    car=car,
                    image=image_file,
                    caption=caption
                )

        # Handle images from your JS multi-upload
        # In our JS example, all images are in a single input, so we need to loop:
        more_images = request.FILES.getlist('more-images-input')
        for idx, img in enumerate(more_images):
            caption = request.POST.get(f'image_caption_{idx}', '')
            NewCarImage.objects.create(
                car=car,
                image=img,
                caption=caption
            )

        messages.success(request, 'موتر با موفقیت اضافه شد.')
        return redirect('home:dashboard')  

    return render(request, 'products/add-listing.html')