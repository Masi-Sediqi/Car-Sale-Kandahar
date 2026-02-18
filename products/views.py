from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib import messages
from django.db.models import Q, Case, When, Value, IntegerField
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
            user=request.user,
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
        return redirect('users:profile', id=request.user.id)  

    return render(request, 'products/add-listing.html')


def delete_car(request, id):
    car = get_object_or_404(NewCar, id=id)
    car.delete()

    messages.success(request, 'موتر ذیل موفقانه حذف شد')

    return redirect(request.META.get('HTTP_REFERER', '/'))


def car_detail(request, id):
    car = get_object_or_404(NewCar.objects.prefetch_related('images'), id=id)
    return render(request, 'products/car-detail.html', {'car': car})


def shop(request):
    query = request.GET.get('q', '').strip()

    cars = NewCar.objects.filter(is_activated=True)

    if query:
        # Annotate priority for ordering: exact title or description first
        cars = cars.annotate(
            priority=Case(
                When(title__iexact=query, then=Value(1)),          # exact title match -> highest
                When(description__iexact=query, then=Value(1)),    # exact description match -> highest
                When(title__icontains=query, then=Value(2)),       # partial title match -> medium
                When(description__icontains=query, then=Value(2)), # partial description match -> medium
                When(year_of_manufacture__icontains=query, then=Value(3)),
                When(fuel_type__icontains=query, then=Value(3)),
                When(gearbox_type__icontains=query, then=Value(3)),
                When(price__icontains=query, then=Value(3)),
                When(mileage_km__icontains=query, then=Value(3)),
                default=Value(4),  # everything else
                output_field=IntegerField()
            )
        ).filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(year_of_manufacture__icontains=query) |
            Q(fuel_type__icontains=query) |
            Q(gearbox_type__icontains=query) |
            Q(price__icontains=query) |
            Q(mileage_km__icontains=query)
        ).order_by('priority', '-created_at')  # first priority, then newest

    else:
        cars = cars.order_by('-created_at')

    context = {
        'cars': cars,
        'query': query,
    }
    return render(request, 'products/shop.html', context)