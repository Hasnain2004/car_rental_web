from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Booking, ContactMessage
from datetime import datetime, timedelta
from django.utils import timezone

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number', 'address', 'driver_license', 'profile_picture', 'date_of_birth']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

class BookingForm(forms.ModelForm):
    DURATION_CHOICES = [
        (1, '1 Day'),
        (2, '2 Days'),
        (3, '3 Days'),
        (4, '4 Days'),
        (5, '5 Days'),
        (7, '1 Week'),
        (14, '2 Weeks'),
        (30, '1 Month'),
    ]
    
    PICKUP_TIME_CHOICES = [
        ('9:00', '9:00 AM'),
        ('10:00', '10:00 AM'),
        ('11:00', '11:00 AM'),
        ('12:00', '12:00 PM'),
        ('13:00', '1:00 PM'),
        ('14:00', '2:00 PM'),
        ('15:00', '3:00 PM'),
        ('16:00', '4:00 PM'),
        ('17:00', '5:00 PM'),
    ]
    
    pickup_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="Select the pickup date"
    )
    
    pickup_time = forms.ChoiceField(
        choices=PICKUP_TIME_CHOICES,
        help_text="Select the pickup time"
    )
    
    rental_duration = forms.ChoiceField(
        choices=DURATION_CHOICES,
        help_text="Select rental duration"
    )
    
    class Meta:
        model = Booking
        fields = ['pickup_date', 'pickup_time', 'rental_duration']
    
    def clean(self):
        cleaned_data = super().clean()
        pickup_date = cleaned_data.get('pickup_date')
        pickup_time = cleaned_data.get('pickup_time')
        rental_duration = cleaned_data.get('rental_duration')
        
        if pickup_date and pickup_time and rental_duration:
            # Convert pickup_date to datetime with the selected pickup_time
            hour, minute = map(int, pickup_time.split(':'))
            pickup_datetime = datetime.combine(
                pickup_date, 
                datetime.min.time().replace(hour=hour, minute=minute)
            )
            
            # Convert to timezone-aware datetime
            pickup_datetime = timezone.make_aware(pickup_datetime)
            
            # Check if pickup date is in the past
            if pickup_datetime < timezone.now():
                raise forms.ValidationError("Pickup date and time cannot be in the past")
            
            # Calculate end_date based on duration
            end_datetime = pickup_datetime + timedelta(days=int(rental_duration))
            
            # Add the calculated start and end dates to cleaned_data
            cleaned_data['start_date'] = pickup_datetime
            cleaned_data['end_date'] = end_datetime
        
        return cleaned_data

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['subject', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5}),
        } 