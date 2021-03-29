import datetime

from django.shortcuts import render, redirect
from .models import ImageProcessorModel
from .forms import ImageProcessorForm
from django.contrib import messages
from django.middleware import csrf
from django.http import JsonResponse

from .tasks import add_waterMark


def home(request):
    return render(request, 'imageProcessorApp/home.html', {})


def image_list(request):
    all_uploaded_image_data = ImageProcessorModel.objects.all()
    return render(request, 'imageProcessorApp/image_list.html', {'image_data': all_uploaded_image_data})


def image_upload(request):
    form = ImageProcessorForm()
    if request.method == 'POST':
        form = ImageProcessorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, ('New image has been added!'))
            return render(request, 'imageProcessorApp/image_upload.html', {})
    context = {'form': form}
    return render(request, 'imageProcessorApp/image_upload.html', context)


def reject_pic(request, photo_id):
    if(photo_id is None):
        messages.error(
            request, ('Unrecognized input was sent. Please check and try again.'))
        return JsonResponse({"error": "error"}, status=400)
    try:
        Photo = ImageProcessorModel.objects.get(id=photo_id)
    except ImageProcessorModel.DoesNotExist:
        messages.error(request, ('Unable to get object from DB.'))
        return JsonResponse({"error": "error"}, status=400)
    Photo.image_verified = True
    Photo.image_rejected = True
    Photo.save()
    # call a celery task that runs in background
    # task should be async to prevent view from blocking
    add_waterMark.apply_async(expires=datetime.datetime.now() + datetime.timedelta(
        minutes=5), countdown=10, kwargs={"photo_id": photo_id, "selected_flag": "rejected"})
    messages.success(
        request, ('Image with ID: {} was rejected successfully'.format(int(photo_id))))
    return JsonResponse({"sucess": "sucessfully"}, status=200)


def accept_pic(request, photo_id):
    if(photo_id is None):
        messages.error(
            request, ('Unrecognized input was sent. Please check and try again.'))
        return JsonResponse({"error": "error"}, status=400)
    try:
        Photo = ImageProcessorModel.objects.get(id=photo_id)
    except ImageProcessorModel.DoesNotExist:
        messages.error(request, ('Unable to get object from DB.'))
        return JsonResponse({"error": "error"}, status=400)
    Photo.image_verified = True
    Photo.image_rejected = False
    Photo.save()
    add_waterMark.apply_async(expires=datetime.datetime.now() + datetime.timedelta(
        minutes=5), countdown=10, kwargs={"photo_id": photo_id, "selected_flag": "accepted"})
    messages.success(
        request, ('Image with ID: {} was accepted successfully'.format(int(photo_id))))
    return JsonResponse({"sucess": "sucessfully"}, status=200)


def image_view(request):
    # filter and only show unverified images in the image viewer tab
    Photo = ImageProcessorModel.objects
    all_unverified_photos = Photo.filter(image_verified=False)
    if(all_unverified_photos.count() == 0):
        messages.error(
            request, ('All images have been verified. Please upload new content'))
        return render(request, 'imageProcessorApp/image_view.html', {})

    context = {
        'image_info': all_unverified_photos,
        'image_length': len(all_unverified_photos),
        'csrf_token': csrf.get_token(request)

    }
    return render(request, 'imageProcessorApp/image_view.html', context)


def single_image_view(request, photo_id=None):
    # filter and only show unverified images in the image viewer tab
    Photo = ImageProcessorModel.objects
    all_unverified_photos = Photo.filter(image_verified=False)
    # print(all_unverified_photos[0].image_verified)
    if(all_unverified_photos.count() == 0):
        messages.error(
            request, ('All images have been verified. Please upload new content'))
        return render(request, 'imageProcessorApp/image_view.html', {})

    context = {
        'image_info': all_unverified_photos.get(id=int(photo_id)),
        'next_image_id': int(photo_id) + 1,
    }

    return render(request, 'imageProcessorApp/image_view.html', context)

# handle server errors
# handle client errors


def error_404(request):
    return render(request, 'imageProcessorApp/error_404.html', {})


def error_500(request):
    return render(request, 'imageProcessorApp/error_500.html', {})


# Helpers
