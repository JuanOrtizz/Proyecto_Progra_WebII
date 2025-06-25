from decouple import config
from django.contrib.auth import get_user_model
from django.db.utils import OperationalError

try:
    User = get_user_model()
    #Obtengo las credenciales del .env
    username = config("DJANGO_SUPERUSER_USERNAME")
    email = config("DJANGO_SUPERUSER_EMAIL")
    password = config("DJANGO_SUPERUSER_PASSWORD")

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )
        print("Superusuario creado.")
    else:
        print("El superusuario ya existe.")

except OperationalError:
    print("La DB aún no está lista. Intenta de nuevo tras migraciones.")