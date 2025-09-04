from django.contrib.auth.decorators import user_passes_test

def administrador_required(view_func):
    # Permito el acceso a los administradores (dueño de la pagina)
    return user_passes_test(
        lambda u: u.is_authenticated and (u.is_superuser or u.groups.filter(name='administrador').exists())
    )(view_func)