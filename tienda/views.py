from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetConfirmView, PasswordChangeView, PasswordResetView
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseForbidden
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .forms import ContactoForm, ProductoForm, RegistroForm, ValidarCodigoForm
from .models import Consultas, Productos, UsuariosPermitidos
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from .serializers import ConsultasSerializer, ProductosSerializer
from django.contrib.auth.models import User
from django.urls import reverse
import requests
import os
from django.templatetags.static import static
from django.conf import settings
from django.http import HttpResponse, Http404
from django.views import View
import mimetypes

#Vista index
def pagina_index(request):
    return render(request, 'tienda/index.html', {'repeticiones': range(10)})

#Vista colecciones
def colecciones(request):
    return render(request, 'tienda/colecciones.html')

#vista locales
def locales(request):
    return render(request, 'tienda/locales.html')

#Vista Contacto (Formulario)
def contacto(request):
    if request.method == "POST":  # Si el metodo de respuesta es post
        form = ContactoForm(request.POST)
        #Verifico si el form es valido
        if form.is_valid():
            #Obtengo los datos del formulario
            nombre = form.cleaned_data["nombre"].strip()
            email = form.cleaned_data["email"].strip()
            telefono = form.cleaned_data["telefono"].strip()
            mensaje = form.cleaned_data["mensaje"].strip()
            # Verifico que categoria de mensaje es, con la funcion clasificar_mensaje
            categoria_mensaje = clasificar_mensaje(mensaje)

            #Guardo en la DB
            consulta = Consultas(
                nombre = nombre,
                telefono = telefono,
                email = email,
                mensaje = mensaje,
                categoria_detectada = categoria_mensaje
            )
            consulta.save()

            #try-catch para enviar el mail
            try:
                # Renderizo el template del email con contexto para mandar por el email
                context = {
                    'nombre': nombre,
                    'email': email,
                    'telefono': telefono,
                    'categoria_mensaje': categoria_mensaje,
                    'mensaje': mensaje
                }

                # declaro variables con los valores para el mail
                asunto = f"Recibimos tu {categoria_mensaje}. Fresh & Simple"
                mensaje_email = "Si no se visualiza correctamente contacta con nosotros"
                # obtengo el mensaje html mediante la plantilla y le paso todas las variables que necesita la plantilla por el contexto
                mensaje_html = render_to_string('tienda/emails/contacto_email.html', context)
                destinatario = email
                # envio el mail
                send_mail(asunto, mensaje_email, settings.EMAIL_HOST_USER, [destinatario], fail_silently=False, html_message=mensaje_html)
            except Exception as e:
                return JsonResponse({"success": False, "errors": f"Error al enviar correo: {e}"})

            return JsonResponse({"success": True,"message": f"Recibimos tu mensaje y te estaremos contactando al email {email}"})
        else:
            return JsonResponse({"success": False,"errors": form.errors})
    else:
        form = ContactoForm()

    return render (request, 'tienda/contacto.html', {'form': form})

#Vista colecciones filtradas (Por coleccion)
def coleccion_filtrada(request, tipo):
    valores = {
        'pantalones': '1',
        'remeras': '2',
        'tops': '3',
        'vestidos': '4',
        'buzos': '5',
        'camperas': '6',
        'accesorios': '7',
    }
    tipo_singular = valores.get(tipo.lower())
    prendas = Productos.objects.filter(tipo=tipo_singular) #Filtro productos por tipo

    #Agrego una imagen default si el path de la imagen es invalido o no existe la imagen en media
    for prenda in prendas:
        prenda.imagen_url_final = '/static/tienda/img/default_prenda.webp' #Agrego una imagen default al principio
        if prenda.imagen:
            imagen_path = os.path.join(settings.MEDIA_ROOT, prenda.imagen.name)
            if os.path.exists(imagen_path):
                prenda.imagen_url_final = prenda.imagen.url #Agrego la imagen que le corresponde si existe

    return render(request, 'tienda/coleccion_filtrada.html', {'prendas': prendas,'tipo': tipo.capitalize()})

#Vista registro
def registro(request):
    #redirige al inicio si esta logeado
    if request.user.is_authenticated:
        return redirect('index') #redirige a index.html

    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():

            # Obtengo los datos del formulario
            nombre = form.cleaned_data["nombre"].strip()
            apellido = form.cleaned_data["apellido"].strip()
            email = form.cleaned_data["email"].strip()
            contrasenia = form.cleaned_data["contrasenia"].strip()

            # Verifica en la tabla si hay un usuario permitido con ese email
            try:
                usuario_permitido = UsuariosPermitidos.objects.get(email=email)
            except UsuariosPermitidos.DoesNotExist: # Si no existe devuelve el error informando que no esta autorizado al registro
                return JsonResponse({"success": False, "errors": "Acceso restringido. No estás autorizado."})

            #valido si ya hay un usuario registrado con ese email
            if User.objects.filter(email__iexact=email, is_active=True).exists():
                return JsonResponse({"success":False, "errors": "Ya hay un usuario registrado con este email."})
            elif User.objects.filter(email__iexact=email, is_active=False).exists(): #Usuario nuevo que no completo su validacion.
                usuario = User.objects.get(email__iexact=email) #obtengo el usuario que ya se habia registrado pero no validado
                #le asigno los nuevos valores del formulario por si realiza modificaciones
                usuario.first_name = nombre
                usuario.last_name = apellido
                usuario.set_password(contrasenia)
            else:# Usuario nuevo (no existe en la DB)
                # Creo el usuario de Django
                usuario = User.objects.create_user(
                    username=email,
                    email=email,
                    password=contrasenia,
                    first_name=nombre,
                    last_name=apellido,
                    is_active=False  # le pongo asi para que no pueda iniciar sesion hasta que no valide
                )

            usuario.save()
            request.session['usuario_a_validar'] = usuario.id  # guardo el id en sesion

            # enviar mail con el codigo
            try:
                # Renderizo el template del email con contexto para mandar por el email
                context = {
                    'nombre': nombre,
                    'codigo' : usuario_permitido.codigo_validacion
                }

                # declaro variables con los valores para el mail
                asunto = "Validación de cuenta - Fresh & Simple"
                mensaje_texto = f"Tu código de validación es: {usuario_permitido.codigo_validacion}\n\nPor favor, ingresa este código en el sitio para validar tu cuenta."
                # obtengo el mensaje html mediante la plantilla y le paso todas las variables que necesita la plantilla por el contexto
                mensaje_html = render_to_string('tienda/emails/registro_email.html', context)
                destinatario = email
                send_mail(asunto, mensaje_texto, settings.EMAIL_HOST_USER, [destinatario], fail_silently=False, html_message=mensaje_html)
                return JsonResponse({'success': True, 'message': "Te enviamos un código de verificación de cuenta. A continuación te redirigiremos a la verificación de cuenta...", 'redirect_url': reverse('validar-registro')})
            except Exception as e:
                return JsonResponse({"success": False, "errors": f"Error al enviar correo: {e}"})
        else:
            return JsonResponse({"success": False, "errors": form.errors})
    else:
        form = RegistroForm()
    return render(request, 'tienda/registro.html', {'form': form})

#Vista validar registro
def validar_registro(request):
    #redirige al inicio si esta logeado
    if request.user.is_authenticated:
        return redirect('index') #redirige a index.html

    id_usuario = request.session.get('usuario_a_validar')

    # si no hay datos en la sesion denego el acceso
    if not id_usuario:
        return HttpResponseForbidden("Acceso no autorizado.")

    if request.method == 'POST':
        form = ValidarCodigoForm(request.POST)
        if form.is_valid():
            codigo = form.cleaned_data['codigo'].strip() #Capturo el codigo del formulario

            #Obtengo el usuario
            usuario_validado = User.objects.get(id=id_usuario)
            if not usuario_validado:
                return JsonResponse({"success": False, "errors": "Usuario inválido."})

            #Si el usuario ya esta registrado
            if usuario_validado.is_active:
                return JsonResponse({'success': False, 'errors': "Ya hay una cuenta registrada con este email."})

            #Si el codigo no es valido
            if not UsuariosPermitidos.objects.filter(email__iexact = usuario_validado.email , codigo_validacion=codigo).exists():
                return JsonResponse({'success': False, 'errors': "Código inválido."})

            # Actualizo el usuario en la DB como activo
            usuario_validado.is_active=True
            usuario_validado.save()

            #Vacio los datos de sesion
            del request.session['usuario_a_validar']

            return JsonResponse({'success': True, 'message': "Cuenta validada. Ya podés iniciar sesión con tu email y contraseña. A continuación te redirigiremos al login...",'redirect_url': reverse('login')})
        else:
            return JsonResponse({"success": False, "errors": form.errors})
    else:
        form = ValidarCodigoForm()
    return render(request, 'tienda/validar_registro.html', {'form': form})

#Vista Dashboard
@login_required()
def dashboard (request):
    return render(request, 'tienda/dashboard.html')

#vista Consultas
@login_required()
def consultas(request):
    consultas_lista = Consultas.objects.all()
    contador_consultas_total = 0
    contador_consultas_comerciales = 0
    contador_consultas_tecnicas = 0
    contador_consultas_rrhh = 0
    contador_consultas_generales = 0
    for consulta in consultas_lista:
        categoria = consulta.categoria_detectada.strip().lower()
        contador_consultas_total+=1
        match categoria:
            case "consulta comercial":
                contador_consultas_comerciales+=1
            case "consulta técnica":
                contador_consultas_tecnicas+=1
            case "consulta de rrhh":
                contador_consultas_rrhh+=1
            case _:
                contador_consultas_generales+=1
    return render(request, 'tienda/consultas.html', {'consultas': consultas_lista, 'total_consultas': contador_consultas_total, 'consultas_comerciales': contador_consultas_comerciales, 'consultas_tecnicas': contador_consultas_tecnicas, 'consultas_rrhh' : contador_consultas_rrhh, 'consultas_generales' :contador_consultas_generales})

#Vista Productos
@login_required()
def productos(request):
    #Filtro para filtrar mediante el select los productos registrados
    tipo_filtro = request.GET.get('tipo', '')
    productos_lista = Productos.objects.all()
    if tipo_filtro:
        productos_lista = productos_lista.filter(tipo=tipo_filtro)

    return render(request, 'tienda/productos.html', {'productos': productos_lista, 'tipo_filtro': tipo_filtro})

#Vista registrar producto
@login_required()
def registrar_producto(request):
    if request.method == "POST":  # Si el metodo de respuesta es post
        form = ProductoForm(request.POST, request.FILES)
        #Verifico si el form es valido
        if form.is_valid():

            #Obtengo los datos del formulario
            nombre = form.cleaned_data["nombre"].strip()
            precio = form.cleaned_data["precio"].strip()
            tipo = form.cleaned_data["tipo"].strip()
            imagen = form.cleaned_data['imagen'].strip()

            if Productos.objects.filter(nombre = nombre).exists():
                return JsonResponse({"success": False, "errors": "Ya existe un producto con ese nombre."})

            #Guardo en la DB
            producto = Productos(
                nombre = nombre,
                precio = precio,
                tipo = tipo,
                imagen = imagen
            )
            producto.save()

            return JsonResponse({"success": True,"message": f"Se registró con éxito el producto {nombre}"})
        else:
            return JsonResponse({"success": False, "errors": form.errors})
    else:
        form = ProductoForm()
    return render (request, 'tienda/registrar_producto.html', {'form': form})

#Vista modificar producto
@login_required()
def modificar_producto(request, producto_id):
    producto = get_object_or_404(Productos, id=producto_id) # obtengo el Producto

    if request.method == 'POST':
        form = ProductoForm(request.POST, files=request.FILES, imagen_actual=producto.imagen)
        form.fields['imagen'].required = False
        if form.is_valid():
            #obtengo los valores (antiguos) del formulario
            nombre_antiguo = producto.nombre
            precio_antiguo = producto.precio

            # obtengo los datos del formulario que pudo haber realizado cambios
            producto.nombre = form.cleaned_data["nombre"].strip()
            producto.precio = form.cleaned_data["precio"].strip()

            if producto.nombre == nombre_antiguo and producto.precio == precio_antiguo:
                return JsonResponse({"success": False, "errors": "No realizaste modificaciones."})
            elif Productos.objects.filter(nombre=producto.nombre).exclude(id=producto.id).exists():
                return JsonResponse({"success": False, "errors": "Ya existe un producto con ese nombre."})
            else:
                # actualizo los valores de la consulta
                producto.save()
            return JsonResponse({"success": True, "message": "Producto modificado con éxito."})
        else:
            return JsonResponse({"success": False, "errors": form.errors})
    else:
        #lleno el formulario con los datos actuales del producto
        form = ProductoForm(initial={
            'nombre': producto.nombre,
            'precio': producto.precio,
            'tipo': producto.tipo,
            'imagen': producto.imagen
        })

        #Le pongo al campo tipo un atributo readonly para evitar su modificacion
        form.fields['tipo'].readonly = True

    return render(request, 'tienda/modificar_producto.html', {'form': form})

#vista Eliminar producto
@login_required()
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Productos, id=producto_id)

    #Elimino la imagen del directorio
    if producto.imagen:
        imagen_path = producto.imagen.path
        if os.path.isfile(imagen_path):
            os.remove(imagen_path)

    #Elimino el producto de la DB
    producto.delete()

    return JsonResponse({"success": True})

#Vista Modificar Consulta
@login_required()
def modificar_consulta(request, consulta_id):
    consulta = get_object_or_404(Consultas, id=consulta_id) # obtengo la Consulta

    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            #obtengo los valores (antiguos) del formulario
            email_antiguo = consulta.email
            telefono_antiguo = consulta.telefono

            # obtengo los datos del formulario que puede cambiar (actuales)
            consulta.email = form.cleaned_data["email"].strip()
            consulta.telefono = form.cleaned_data["telefono"].strip()

            if consulta.email == email_antiguo and consulta.telefono == telefono_antiguo:
                return JsonResponse({"success": False, "errors": "No realizaste modificaciones."})
            else:
                # actualizo los valores de la consulta
                consulta.save()
            return JsonResponse({"success": True, "message": "Consulta modificada con éxito."})
        else:
            return JsonResponse({"success": False, "errors": form.errors})
    else:
        #lleno el formulario con los datos actuales de la consulta
        form = ContactoForm(initial={
            'nombre': consulta.nombre,
            'email': consulta.email,
            'telefono': consulta.telefono,
            'mensaje': consulta.mensaje
        })

        #creo un array con los campos del formulario
        campos_readonly = [
            'nombre',
            'mensaje'
        ]

        #for para ponerle a esos campos un atributo readonly para evitar su modificacion
        for campo in campos_readonly:
            form.fields[campo].widget.attrs['readonly'] = True

    return render(request, 'tienda/modificar_consulta.html', {'form': form})

#Vista para eliminar una consulta
@login_required()
def eliminar_consulta(request, consulta_id):
    consulta = get_object_or_404(Consultas, id = consulta_id)
    consulta.delete() #elimino la consulta

    #Actualizo los contadores
    contador_consultas_total = Consultas.objects.count()
    contador_consultas_comerciales = Consultas.objects.filter(categoria_detectada="Consulta Comercial").count()
    contador_consultas_tecnicas = Consultas.objects.filter(categoria_detectada="Consulta Técnica").count()
    contador_consultas_rrhh = Consultas.objects.filter(categoria_detectada="Consulta de RRHH").count()
    contador_consultas_generales = Consultas.objects.filter(categoria_detectada="Consulta General").count()

    return JsonResponse({"success": True, 'total_consultas': contador_consultas_total, 'consultas_comerciales': contador_consultas_comerciales, 'consultas_tecnicas': contador_consultas_tecnicas, 'consultas_rrhh' : contador_consultas_rrhh, 'consultas_generales' :contador_consultas_generales})

# clase para el viewSet de Consultas
class ConsultasViewSet(viewsets.ModelViewSet):
    queryset =  Consultas.objects.all()
    serializer_class = ConsultasSerializer
    permission_classes = [IsAuthenticated] #Protejo los endpoint, si no elogeado desde dashboard no puede acceder en un futuro se usara JWT

# clase para el viewSet de Productos
class ProductosViewSet(viewsets.ModelViewSet):
    queryset =  Productos.objects.all()
    serializer_class = ProductosSerializer
    permission_classes = [IsAuthenticated] #Protejo los endpoint, si no esta logeado desde dashboard no puede acceder en un futuro se usara JWT

#Clase para obtener datos de la api ZenQuotes (frases)
class ObtenerFraseAPIView(APIView):
    def get(self, request):
        # obtengo frase
        url = "https://zenquotes.io/api/quotes/"
        response = requests.get(url)

        # Si no pudo obtener la frase
        if response.status_code != 200:
            return Response({"error": "No se pudo obtener la frase"}, status=500)

        # Transformo la data a json
        data = response.json()

        # Si la api da una respuesta invalida
        if not data or not isinstance(data, list):
            return Response({"error": "Respuesta inválida de la API"}, status=500)

        # Obtengo la data en un objeto frase
        frase_obj = data[0]
        frase = frase_obj.get('q') # Obtengo la frase

        # devuelo la respuesta (frase) al frontend
        return Response({"frase": frase})

#Sobreescribo la clase PasswordResetView de Autenticacion de Django para personalizacion (Actua como recuperar cuenta)
class CustomPasswordResetView(PasswordResetView):
    template_name = 'tienda/recuperar_cuenta.html' # plantilla que usa

    #funcion para redirigir a inicio si esta logeado
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')  # redirige a index.html
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form): # funcion para validar el formulario
        email = form.cleaned_data['email'].strip() #obtengo el email
        self.request.session['reset_email'] = email #lo guardo en la sesion

        # Busco el usuario con ese email
        users = User.objects.filter(email=email, is_active=True)
        if not users.exists(): # Si el usuario no existe o su cuenta no esta activa
            return JsonResponse({'success': False, 'errors': f"No hay ningún usuario registrado con ese email."})

        #Si existe, obtengo el usuario
        usuario = users.first()

        # Genero los tokens para el link para mayor seguridad
        uid = urlsafe_base64_encode(force_bytes(str(usuario.pk)))
        token = default_token_generator.make_token(usuario)

        # Renderizo el template del email con contexto para mandar por el email
        context = {
            'usuario': usuario,
            'protocolo': 'https' if self.request.is_secure() else 'http',
            'dominio': self.request.get_host(),
            'uid': uid,
            'token': token,
        }

        logo_url = f"{context['protocolo']}://{context['dominio']}{static('img/logo_fys.webp')}"
        context['logoUrl'] = logo_url
        # Mando el mail
        try:
            # obtengo el mensaje html mediante la plantilla y le paso todas las variables que necesita la plantilla por el contexto
            message_html = render_to_string('tienda/emails/cambiar_contrasenia_email.html', context)
            send_mail(
                subject='Recuperar contraseña - Fresh & Simple',
                message='',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
                html_message=message_html,
            )
            return JsonResponse({'success': True, 'message': f"Te enviamos los pasos para cambiar tu contraseña al email {email}."})
        except Exception as e:
            return JsonResponse({"success": False, "errors": f"Error al enviar correo: {e}"})

    def form_invalid(self, form):
        return JsonResponse({'success': False, 'errors': form.errors})

#Sobreescribo la clase PasswordResetConfirmView de Autenticacion de Django para personalizacion (Actua como Cambiar contraseña "Recuperar cuenta")
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'tienda/cambiar_contrasenia.html'

    #funcion para redirigir a inicio si esta logeado
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')  # redirige a index.html
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return JsonResponse({'success': True,'message': "Cambiaste tu contraseña con éxito. A continuación te redirigiremos al login...",'redirect_url': reverse('login')})

    def form_invalid(self, form):
        return JsonResponse({'success': False, 'errors': form.errors})

#Sobreescribo la clase PasswordResetView de Autenticacion de Django para personalizacion (Actua como cambiar contraseña (Desde el perfil))
class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'tienda/cambiar_contrasenia.html'

    def form_valid(self, form):
        form.save()
        return JsonResponse({'success': True,'message': "Cambiaste tu contraseña con éxito. A continuación te redirigiremos al login...",'redirect_url': reverse('login')})

    def form_invalid(self, form):
        return JsonResponse({'success': False, 'errors': form.errors})

#Clase para servir los archivos con DEBUG=FALSE en produccion
class MediaServeView(View):
    def get(self, request, path):
        full_path = os.path.join(settings.MEDIA_ROOT, path)
        if os.path.exists(full_path):
            with open(full_path, 'rb') as f:
                mime_type, _ = mimetypes.guess_type(full_path)
                return HttpResponse(f.read(), content_type=mime_type)
        raise Http404()

# Funcion auxiliar para clasificar mensaje en la vista Contacto
def clasificar_mensaje(mensaje):
    mensaje = mensaje.lower()
    categorias = {
        "Consulta Comercial": ["precio", "costo", "tarifa", "compra"],
        "Consulta Técnica": ["soporte", "error", "problema", "ayuda"],
        "Consulta de RRHH": ["trabajo", "cv", "empleo", "linkedin"]
    }
    for categoria, palabras in categorias.items():
        if any(palabra in mensaje for palabra in palabras):
            return categoria
    return "Consulta General"