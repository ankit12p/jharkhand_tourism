from django.apps import AppConfig


class TourismConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tourism'

    def ready(self):
        # This code runs once when the app is ready.
        from django.contrib.auth.models import User

        # Create a dummy admin user if one doesn't exist
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'adminpassword')
            print("Created dummy admin: username='admin', password='adminpassword'")

        # Create a dummy regular user if one doesn't exist
        if not User.objects.filter(username='user').exists():
            User.objects.create_user('user', 'user@example.com', 'userpassword')
            print("Created dummy user: username='user', password='userpassword'")
