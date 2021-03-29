from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('image_list', views.image_list, name='image_list'),
    path('image_upload', views.image_upload, name='image_upload'),
    path('image_view/<int:photo_id>', views.single_image_view, name='single_image_view'),
    path('image_view', views.image_view, name='image_view'),
    path('accept_pic/<int:photo_id>', views.accept_pic, name='accept_pic'),
    path('reject_pic/<int:photo_id>', views.reject_pic, name='reject_pic'),

    #django readiness probe
    path('readiness', views.home, name='readiness'),

]
