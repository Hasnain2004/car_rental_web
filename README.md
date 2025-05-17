# Car Rental Website

A Django-based car rental platform with user authentication, booking management, and a responsive design.

## Features

- User registration and profile management
- Car browsing with search and filtering
- Booking system with date selection
- Booking management (view, cancel)
- Admin panel for managing cars, bookings, and users
- Responsive design for all devices

## Installation

### Prerequisites

- Python 3.8+
- pip
- virtualenv (recommended)

### Setup

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/car_rental_web.git
   cd car_rental_web
   ```

2. Create and activate a virtual environment:

   ```
   python -m venv venv

   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root directory with the following variables (adjust as needed):

   ```
   DJANGO_SECRET_KEY=your_secret_key_here
   DJANGO_DEBUG=True
   DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
   ```

5. Apply migrations:

   ```
   python manage.py migrate
   ```

6. Create a superuser:

   ```
   python manage.py createsuperuser
   ```

7. Create the media directory:

   ```
   mkdir -p media/car_images media/profile_pics
   ```

8. Run the development server:

   ```
   python manage.py runserver
   ```

9. Access the site at http://127.0.0.1:8000/

## Usage

### Admin Access

1. Go to http://127.0.0.1:8000/admin/
2. Log in with the superuser credentials created earlier
3. Add cars, manage bookings, and users

### Regular User Access

1. Register a new account at http://127.0.0.1:8000/register/
2. Browse available cars and make bookings
3. Manage your profile and view your booking history

## Deployment to Production

For production deployment:

1. Set environment variables:

   ```
   DJANGO_SECRET_KEY=your_secure_secret_key
   DJANGO_DEBUG=False
   DJANGO_ALLOWED_HOSTS=your-domain.com
   ```

2. Configure PostgreSQL database in settings.py
3. Set up static files serving with a web server like Nginx
4. Use Gunicorn or uWSGI as the application server

## License

This project is licensed under the MIT License - see the LICENSE file for details.
