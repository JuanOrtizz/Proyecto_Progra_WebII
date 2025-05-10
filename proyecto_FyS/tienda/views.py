from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def pagina_tienda_fys(request):
    mensaje = "" # inicializo la variable mensaje en str

    if request.method == "POST": # Si el metodo de respuesta es post
        nombre = request.POST.get("nombre") # guarda el nombre, telefono, email, categoria y mensaje del usuario
        telefono = request.POST.get("telefono")
        email = request.POST.get("email")
        categoria = request.POST.get("categoria")
        mensaje_usuario = request.POST.get("mensaje_usuario")

        mensaje = f"Gracias {nombre}, recibimos tu mensaje y te estaremos contactando al email {email}" # guardo en la variable mensaje el siguiente mensaje

    return render(request, 'tienda/index.html', {"mensaje": mensaje}) #devuelvo la respuesta (mensaje) a index.html

def sucursales(request):
    return render(request, 'tienda/sucursales.html') # cree la vista de la pagina sucursales