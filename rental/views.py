from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from datetime import datetime, timedelta

from .models import Car, Booking, Profile, ContactMessage
from .forms import (
    UserRegisterForm, UserUpdateForm, ProfileUpdateForm,
    BookingForm, ContactForm
)

# Helper function to check if user is admin
def is_admin(user):
    if user.is_authenticated:
        try:
            return user.profile.user_type == 'admin'
        except Profile.DoesNotExist:
            return False
    return False

# Helper function to update car availability based on bookings
def update_car_availability(car_id=None):
    """Update car availability based on current bookings"""
    now = timezone.now()
    
    # Get cars with completed bookings
    if car_id:
        cars = Car.objects.filter(id=car_id)
    else:
        cars = Car.objects.all()
        
    for car in cars:
        # Check if there are any active bookings for this car
        active_bookings = Booking.objects.filter(
            car=car,
            status__in=['pending', 'confirmed'],
            end_date__gt=now
        ).exists()
        
        # If no active bookings, car should be available
        if not active_bookings:
            car.is_available = True
            car.save()

# Welcome page for non-authenticated users
def welcome(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'rental/welcome.html')

# Main pages
@login_required
def home(request):
    # Update car availability
    update_car_availability()
    
    # Get all featured cars that are available
    featured_cars = Car.objects.filter(
        is_available=True,
        featured_on_homepage=True
    ).order_by('-created_at')
    
    context = {
        'featured_cars': featured_cars,
    }
    return render(request, 'rental/index.html', context)

@login_required
def about(request):
    return render(request, 'rental/about.html')

@login_required
def car_list(request):
    # Update car availability
    update_car_availability()
    
    # Get all available cars
    cars = Car.objects.filter(is_available=True)
    
    # Handle search filters
    search_query = request.GET.get('q', '')  # Default to empty string instead of None
    category_filter = request.GET.get('category')
    
    if search_query:
        cars = cars.filter(
            Q(make__icontains=search_query) | 
            Q(model__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    if category_filter and category_filter != 'all':
        cars = cars.filter(category=category_filter)
    
    # Get all categories for the filter dropdown
    categories = Car.CATEGORY_CHOICES
    
    # Organize cars by category if no specific category is selected
    category_cars = {}
    if not category_filter or category_filter == 'all':
        for category_id, category_name in categories:
            category_cars[category_id] = {
                'name': category_name,
                'cars': cars.filter(category=category_id)
            }
        
        # Paginate the results only when a specific category is selected
        page_obj = None
    else:
        # Paginate the results
        paginator = Paginator(cars, 6)  # Show 6 cars per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        category_cars = None
    
    context = {
        'page_obj': page_obj,
        'category_cars': category_cars,
        'search_query': search_query,
        'selected_category': category_filter or 'all',
        'categories': categories,
    }
    return render(request, 'rental/car_list.html', context)

@login_required
def car_detail(request, car_id):
    # Update this car's availability
    update_car_availability(car_id)
    
    car = get_object_or_404(Car, id=car_id)
    
    # Get car images
    car_images = car.images.all()
    
    # Get related cars (same make or model)
    related_cars = Car.objects.filter(
        Q(make=car.make) | Q(model=car.model)
    ).exclude(id=car.id)[:3]
    
    context = {
        'car': car,
        'car_images': car_images,
        'related_cars': related_cars,
    }
    return render(request, 'rental/car_detail.html', context)

@login_required
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            if request.user.is_authenticated:
                message.user = request.user
            message.save()
            messages.success(request, 'Your message has been sent. We will get back to you soon!')
            return redirect('contact')
    else:
        form = ContactForm()
    
    context = {
        'form': form,
    }
    return render(request, 'rental/contact.html', context)
def login_view(request):
    if request.user.is_authenticated:
        return render(request, 'login.html')
    return render(request, 'login.html')
# Authentication views
def login_view(request):
    # Redirect if user is already logged in
    if request.user.is_authenticated:
        # Check if the user is admin
        if is_admin(request.user):
            messages.warning(request, "Admin users cannot access the main site. Please log in as a regular user.")
            return redirect('logout')
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Check if the user is admin
            if is_admin(user):
                messages.warning(request, "Admin users cannot access the main site. Please log in as a regular user.")
                return redirect('login')
            
            login(request, user)
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'rental/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('welcome')

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Profile should be created automatically via signals
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}. You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    
    context = {
        'form': form,
    }
    return render(request, 'rental/register.html', context)

# User profile views
@login_required
def profile(request):
    # Get user's bookings
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'bookings': bookings,
        'user': request.user,
    }
    return render(request, 'rental/profile.html', context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        try:
            p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        except Profile.DoesNotExist:
            # Create profile if it doesn't exist
            profile = Profile(user=request.user)
            p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        try:
            p_form = ProfileUpdateForm(instance=request.user.profile)
        except Profile.DoesNotExist:
            p_form = ProfileUpdateForm()
    
    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'rental/edit_profile.html', context)

# Booking views
@login_required
def book_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    
    # Check if car is available
    if not car.is_available:
        messages.error(request, 'This car is not available for booking.')
        return redirect('car_detail', car_id=car.id)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.car = car
            
            # Set start_date and end_date from form's clean method
            booking.start_date = form.cleaned_data['start_date']
            booking.end_date = form.cleaned_data['end_date']
            
            # Check for overlapping bookings
            overlapping_bookings = Booking.objects.filter(
                car=car,
                status__in=['pending', 'confirmed'],
                start_date__lt=booking.end_date,
                end_date__gt=booking.start_date
            ).exists()
            
            if overlapping_bookings:
                messages.error(request, 'This car is already booked for the selected dates.')
                return redirect('book_car', car_id=car.id)
            
            # Calculate total cost
            delta = booking.end_date - booking.start_date
            days = delta.days + 1  # Including the end day
            booking.total_cost = days * car.daily_rate
            
            booking.save()
            
            # Mark car as unavailable during this period
            car.is_available = False
            car.save()
            
            messages.success(request, f'Your booking for {car.year} {car.make} {car.model} has been submitted!')
            return redirect('booking_detail', booking_id=booking.id)
    else:
        # Initialize the form with default values
        tomorrow = timezone.now().date() + timedelta(days=1)
        form = BookingForm(initial={
            'pickup_date': tomorrow,
            'pickup_time': '10:00',  # Default to 10:00 AM
            'rental_duration': 3,    # Default to 3 days
        })
    
    context = {
        'form': form,
        'car': car,
    }
    return render(request, 'rental/book_car.html', context)

@login_required
def booking_list(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'bookings': bookings,
        'now': timezone.now(),
    }
    return render(request, 'rental/booking_list.html', context)

@login_required
def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    context = {
        'booking': booking,
        'now': timezone.now(),
    }
    return render(request, 'rental/booking_detail.html', context)

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    # Only allow cancellation if the booking is pending or confirmed
    if booking.status not in ['pending', 'confirmed']:
        messages.error(request, 'This booking cannot be cancelled.')
        return redirect('booking_detail', booking_id=booking.id)
    
    # Only allow cancellation if the booking start date is in the future
    if booking.start_date <= timezone.now():
        messages.error(request, 'Bookings can only be cancelled before the start date.')
        return redirect('booking_detail', booking_id=booking.id)
    
    if request.method == 'POST':
        booking.status = 'cancelled'
        booking.save()
        
        # Update car availability
        update_car_availability(booking.car.id)
        
        messages.success(request, 'Your booking has been cancelled.')
        return redirect('booking_list')
    
    context = {
        'booking': booking,
    }
    return render(request, 'rental/cancel_booking.html', context)
