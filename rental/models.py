from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Profile(models.Model):
    USER_TYPES = (
        ('customer', 'Customer'),
        ('admin', 'Administrator'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='customer')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    driver_license = models.CharField(max_length=20, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

class Car(models.Model):
    CATEGORY_CHOICES = (
        ('economy', 'Economy'),
        ('standard', 'Standard'),
        ('luxury', 'Luxury'),
        ('suv', 'SUV'),
    )
    
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.IntegerField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='standard')
    license_plate = models.CharField(max_length=15, unique=True)
    color = models.CharField(max_length=20)
    mileage = models.IntegerField()
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='car_images/')  # Kept for backward compatibility
    description = models.TextField()
    featured_on_homepage = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.year} {self.make} {self.model} ({self.get_category_display()})"
    
    @property
    def all_images(self):
        """Get all images for this car, including the main image"""
        images = list(self.images.all())
        # Add main image at the beginning if it exists
        if self.image:
            images.insert(0, {'id': 'main', 'image': self.image, 'is_primary': True})
        return images

class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='car_images/')
    caption = models.CharField(max_length=100, blank=True)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Image for {self.car} - {self.caption if self.caption else 'No caption'}"
    
    class Meta:
        ordering = ['-is_primary', 'created_at']

class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='bookings')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    admin_notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Booking {self.id} - {self.user.username} - {self.car}"
    
    def save(self, *args, **kwargs):
        # Calculate total cost if not already set
        if not self.total_cost:
            delta = self.end_date - self.start_date
            days = delta.days + 1  # Including the end day
            self.total_cost = days * self.car.daily_rate
        super().save(*args, **kwargs)

class ContactMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contact_messages', null=True, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    admin_response = models.TextField(blank=True, null=True)
    
    def __str__(self):
        if self.user:
            return f"Message from {self.user.username}: {self.subject}"
        return f"Anonymous message: {self.subject}"

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile')
    crud_access = models.BooleanField(default=False)
    can_approve_bookings = models.BooleanField(default=False)
    can_manage_users = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Admin: {self.user.username}"
