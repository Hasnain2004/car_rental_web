from django.db import transaction
from .models import Profile

def create_user_profile(backend, user, response, *args, **kwargs):
    """
    Create a user profile for social auth users if it doesn't exist.
    Also update profile information from social auth data.
    """
    if backend.name == 'google-oauth2':
        try:
            with transaction.atomic():
                profile, created = Profile.objects.get_or_create(user=user)
                
                # Update profile with Google data if available
                if created:
                    profile.email = response.get('email', '')
                    profile.first_name = response.get('given_name', '')
                    profile.last_name = response.get('family_name', '')
                    
                    # Get profile picture if available
                    if 'picture' in response:
                        profile.profile_picture = response['picture']
                    
                    profile.save()
                    
        except Exception as e:
            # Log the error but don't break the pipeline
            print(f"Error creating user profile: {str(e)}")
            pass 