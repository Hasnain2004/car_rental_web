from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Welcome page (for non-authenticated users)
    path('', views.welcome, name='welcome'),
    
    # Main pages (authenticated only)
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('cars/', views.car_list, name='car_list'),
    path('cars/<int:car_id>/', views.car_detail, name='car_detail'),
    path('contact/', views.contact, name='contact'),
    
    # User authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    
    # User profile
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    
    # Booking
    path('cars/<int:car_id>/book/', views.book_car, name='book_car'),
    path('bookings/', views.booking_list, name='booking_list'),
    path('bookings/<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('bookings/<int:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),
] 