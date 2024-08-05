from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        username = 'admin'
        email = 'admin@example.com'
        try:
            u = None
            if not get_user_model().objects.filter(username=username).exists() and not User.objects.filter(
                    is_superuser=True).exists():
                print("admin user not found, creating one")

                new_password = "admin"

                u = get_user_model().objects.create_superuser(
                    username, email, new_password)
                print(f"===================================")
                print(
                    f"A superuser '{username}' was created with email '{email}' and password '{new_password}'")
                print(f"===================================")
            else:
                print("admin user found. Skipping super user creation")
                print(u)
        except Exception as e:
            print(f"There was an error: {e}")
