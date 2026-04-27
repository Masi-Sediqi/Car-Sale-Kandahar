from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.models import *
from django.http import JsonResponse, HttpResponse
from django.db.models import Q, Case, When, Value, IntegerField
# Create your views here.

@login_required
def add_listing(request):
    
    if request.method == 'POST':
        # Get main car fields
        title = request.POST.get('title')
        brand_model = request.POST.get('brand_model')
        price = request.POST.get('price')
        year_of_manufacture = request.POST.get('year_of_manufacture')
        gearbox_type = request.POST.get('gearbox_type')
        fuel_type = request.POST.get('fuel_type')
        palet = request.POST.get('palet')
        asnad = request.POST.get('asnad')
        color = request.POST.get('color')
        mileage_km = request.POST.get('mileage_km')
        description = request.POST.get('description')
        main_image = request.FILES.get('main_image')  # optional main image
        mileage_km = request.POST.get('mileage_km')
        mileage_unit = request.POST.get('mileage_unit')
        currency = request.POST.get('currency')

        car = NewCar.objects.create(
            user=request.user,
            title=title,
            price=price,
            palet=palet,
            asnad=asnad,
            color=color,
            year_of_manufacture=year_of_manufacture,
            gearbox_type=gearbox_type,
            fuel_type=fuel_type,
            mileage_unit=mileage_unit,
            mileage_km=mileage_km,
            main_image=main_image,
            currency=currency,
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


@login_required
def edit_car(request, id):
    car = get_object_or_404(NewCar, id=id)

    if car.user != request.user:
        messages.error(request, 'شما اجازه ایدیت این موتر را ندارید.')
        return redirect('products:shop')

    if request.method == 'POST':
        car.title = request.POST.get('title')
        car.price = request.POST.get('price')
        car.currency = request.POST.get('currency')

        car.year_of_manufacture = request.POST.get('year_of_manufacture')
        car.palet = request.POST.get('palet')
        car.asnad = request.POST.get('asnad')
        car.color = request.POST.get('color')

        car.gearbox_type = request.POST.get('gearbox_type')
        car.fuel_type = request.POST.get('fuel_type')

        car.mileage_unit = request.POST.get('mileage_unit')
        car.mileage_km = request.POST.get('mileage_km')

        car.description = request.POST.get('description')

        # اگر checkbox در HTML داری
        car.is_activated = request.POST.get('is_activated') == 'on'

        if request.POST.get('remove_main_image'):
            if car.main_image:
                car.main_image.delete(save=False)
                car.main_image = None

        elif request.FILES.get('main_image'):
            if car.main_image:
                car.main_image.delete(save=False)
            car.main_image = request.FILES['main_image']

        car.save()

        remove_images = request.POST.getlist('remove_images')
        if remove_images:
            images_to_remove = NewCarImage.objects.filter(id__in=remove_images, car=car)
            for img in images_to_remove:
                img.image.delete(save=False)
            images_to_remove.delete()

        for key, value in request.POST.items():
            if key.startswith('caption_'):
                try:
                    image_id = int(key.split('_')[1])
                    image = NewCarImage.objects.get(id=image_id, car=car)
                    image.caption = value
                    image.save()
                except (ValueError, NewCarImage.DoesNotExist):
                    pass

        for key in request.FILES:
            if key.startswith('more_images_'):
                index = key.split('_')[-1]
                image_file = request.FILES[key]
                caption = request.POST.get(f'image_caption_{index}', '')

                NewCarImage.objects.create(
                    car=car,
                    image=image_file,
                    caption=caption
                )

        messages.success(request, 'موتر با موفقیت ایدیت شد.')
        return redirect('users:profile', id=request.user.id)

    return render(request, 'products/car-edit.html', {'car': car})


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

    wishlist_car_ids = []
    if request.user.is_authenticated:
        wishlist_car_ids = Wishlist.objects.filter(
            user=request.user,
            is_active=True
        ).values_list('car_id', flat=True)
        
    else:
        cars = cars.order_by('-created_at')

    context = {
        'cars': cars,
        'query': query,
        'wishlist_car_ids': wishlist_car_ids,
    }
    return render(request, 'products/shop.html', context)


@login_required
def toggle_wishlist(request, car_id):
    car = get_object_or_404(NewCar, id=car_id)
    
    # Check if it's an AJAX request
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user,
        car=car
    )
    
    if created:
        wishlist_item.is_active = True
        wishlist_item.save()
        message = f'موتر "{car.title}" به علاقمندی‌ها اضافه شد.'
        is_active = True
    else:
        wishlist_item.is_active = not wishlist_item.is_active
        wishlist_item.save()
        if wishlist_item.is_active:
            message = f'موتر "{car.title}" دوباره به علاقمندی‌ها اضافه شد.'
        else:
            message = f'موتر "{car.title}" از علاقمندی‌ها حذف شد.'
        is_active = wishlist_item.is_active
    
    # For AJAX requests, return JSON
    if is_ajax:
        return JsonResponse({
            'success': True,
            'is_active': is_active,
            'message': message,
            'car_id': car_id
        })
    
    # For regular requests, redirect as before
    messages.success(request, message) if is_active else messages.warning(request, message)
    return redirect(request.META.get('HTTP_REFERER', 'home:dashboard'))


@login_required
def my_wishlist(request):
    wishlist_items = Wishlist.objects.filter(
        user=request.user,
        is_active=True
    ).select_related('car')

    return render(request, 'products/my_wishlist.html', {
        'wishlist_items': wishlist_items
    })