from django.apps import AppConfig
from django.db.utils import OperationalError
from django.db.models.signals import post_migrate

class YourAppConfig(AppConfig):
    name = 'users'

    def ready(self):
        # We connect the signal to run after migrations are done
        post_migrate.connect(create_default_user, sender=self)



def create_default_user(sender, **kwargs):
    from .models import CustomUser
    try:
        if not CustomUser.objects.filter(username='henok').exists():
            # We use first_name and last_name (Django defaults)
            # instead of fname and lname
            CustomUser.objects.create_superuser(
                username='henok',
                email='henok@example.com',
                password='Super_admin@934',
                phone='0934567890',
                first_name='Henok',
                last_name='Mossie',
                #gender='Male'

            )
            print("--- Default Superuser 'henok' created successfully ---")
    except Exception as e:
        print(f"--- Note: Admin auto-creation skipped: {e} ---")
"""
def create_default_user(sender, **kwargs):
    from .models import CustomUser  
    try:
        # Check if the user already exists to avoid duplicates
        if not CustomUser.objects.filter(username='henok').exists():
            # Use create_superuser so you have full admin access
            CustomUser.objects.create_superuser(
                username='henok',
                email='henok@example.com',
                password='12341234',
                phone='0934567890',
                fname='Default',
                lname='User',
                gender='Other' 

                # DO NOT add fname, lname, or gender here. They are not in CustomUser anymore.
            )
            print("--- Default Superuser 'henok' created successfully ---")
    except Exception as e:
        # This prevents the migrate command from crashing if there's a small issue
        print(f"--- Note: Admin auto-creation skipped: {e} ---")
"""

"""
from django.apps import AppConfig
from django.db.utils import OperationalError
from django.db.models.signals import post_migrate
from django.apps import AppConfig
from django.contrib.auth.hashers import make_password
class YourAppConfig(AppConfig):
    name = 'users'  # Your app name
    def ready(self):
        from .models import CustomUser  # Import inside the ready method
        post_migrate.connect(create_default_user)

def create_default_user(sender, **kwargs):
    from .models import CustomUser  # Import here to avoid AppRegistryNotReady
    try:
        if not CustomUser.objects.filter(username='henok').exists():
            CustomUser.objects.create_user(
                username='henok',
                email='defaultuser@example.com',
                password='12341234',
                phone='0934567890',
                fname='Default',
                lname='User',
                gender='Other'  # Adjust as needed
            )
    except OperationalError:
        pass
"""

"""
def create_default_user(sender, **kwargs):
    from .models import CustomUser  # Import here to avoid AppRegistryNotReady
    try:
        if not CustomUser.objects.filter(username='henok').exists():
            CustomUser.objects.create_user(
                username='henok',
                email='defaultuser@example.com',
                password=make_password('12341234'),  # Ensure password is hashed
                phone='0934567890',
                fname='Default',
                lname='User',
                gender='Other'  # Adjust as needed
            )
    except OperationalError:
        pass
"""
