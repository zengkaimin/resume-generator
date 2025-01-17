from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('builder/', views.builder, name='builder'),
    path('resume/<str:unique_identifier>/', views.resume, name='resume'),
    path('api/generate-festive-image/', views.generate_festive_image, name='generate-festive-image'),
    path('festive-maker/', views.festive_maker, name='festive-maker'),
    path('send-festive-email/', views.send_festive_email, name='send-festive-email'),
]