from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.messages import success
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .forms import ContactoForm, ProductoForm, RegistroForm, ValidarCodigoForm, RecuperarContraseñaForm, \
    CambiarContraseñaForm
from .models import Consultas, Productos, UsuariosPermitidos
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from .serializers import ConsultasSerializer, ProductosSerializer
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
import requests
import os
from django.contrib import messages
from django.shortcuts import redirect

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
def contacto (request):
    if request.method == "POST":  # Si el metodo de respuesta es post
        form = ContactoForm(request.POST)
        #Verifico si el form es valido
        if form.is_valid():
            #Obtengo los datos del formulario
            nombre = form.cleaned_data["nombre"]
            email = form.cleaned_data["email"]
            telefono = form.cleaned_data["telefono"]
            mensaje = form.cleaned_data["mensaje"]
            categoria_mensaje = clasificar_mensaje(mensaje)
            #Verifico que categoria de mensaje es

            #Guardo en la DB
            consultas = Consultas(
                nombre = nombre,
                telefono = telefono,
                email = email,
                mensaje = mensaje,
                categoria_detectada = categoria_mensaje
            )
            consultas.save()

            #try-catch para enviar el mail
            try:
                # declaro variables con los valores para el mail
                asunto = f"Recibimos tu {categoria_mensaje}. Fresh & Simple"
                mensajeEmail = "Si no se visualiza correctamente contacta con nosotros"
                cuerpoMensajeHtml = f"""
                    <html>
                        <body style="font-family: Arial, sans-serif; background-color: #F7F7F7; padding: 30px;">
                            <div style="max-width: 600px; margin: auto; background-color: #FFFFFF; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); border: 1px solid #e0e0e0;">
                                <h2 style="color: #2E8A99; text-align: center;">¡Hola {nombre}!</h2>
                                <p style="font-size: 16px; color: #4A4A4A; text-align: center;">
                                    Hemos recibido tu consulta y nuestro equipo se pondrá en contacto contigo a la brevedad.<br><br>
                                    <strong>Email:</strong> {email}<br><br>
                                    <strong>Teléfono:</strong> {telefono}<br><br>
                                    <strong>Categoría del mensaje:</strong> {categoria_mensaje}<br><br>
                                    <strong>Mensaje enviado:</strong><br>
                                    <em style="display:inline-block; margin-top:10px;">{mensaje}</em>
                                </p>
                                <p style="font-size: 15px; color: #4A4A4A; text-align: center;">
                                     Gracias por comunicarte con <strong style="color: #FF6363;">Fresh & Simple</strong>.
                                </p>
                                <p style="margin-top: 40px; font-size: 12px; text-align: center; color: #888888;">
                                    Si no realizaste esta consulta o necesitas ayuda, por favor contáctanos.
                                </p>
                            </div>
                        </body>
                    </html>
                    """
                destinatario = email
                # envio el mail
                send_mail(asunto, mensajeEmail, settings.EMAIL_HOST_USER, [destinatario], fail_silently=False,html_message=cuerpoMensajeHtml)
            except Exception as e:
                return JsonResponse({"success": False, "errors": f"Error al enviar correo: {e}"})

            return JsonResponse({"success": True,
                                 "message": f"Recibimos tu mensaje y te estaremos contactando al email {email}"})
        else:
            return JsonResponse({"success": False,
                                 "errors": "Error al mandar la consulta, intenta de nuevo"})
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

    # Agrego una imagen default si el path de la imagen es invalido o no existe la imagen en media
    for prenda in prendas:
        imagen_path = os.path.join(settings.MEDIA_ROOT, prenda.imagen.name) if prenda.imagen else None
        if prenda.imagen and os.path.exists(imagen_path):
            prenda.imagen_url_final = prenda.imagen.url
        else:
            prenda.imagen_url_final = '/static/tienda/img/default_prenda.webp'

    return render(request, 'tienda/coleccion_filtrada.html', {'prendas': prendas,'tipo': tipo.capitalize()})

#Vista registro
def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():

            # Obtengo los datos del formulario
            nombre = form.cleaned_data["nombre"]
            email = form.cleaned_data["email"]
            contrasenia = request.POST.get("contraseña")

            #valido si ya hay un usuario registrado con ese email
            if User.objects.filter(email__iexact=email).exists():
                return JsonResponse({"success":False, "errors": "Ya hay un usuario registrado con este email."})

            #Verifica en la tabla si hay un usuario permitido con ese email
            try:
                permitido = UsuariosPermitidos.objects.get(email=email)
                # Guardo datos en sesion
                datos_registro = form.cleaned_data.copy()
                datos_registro['contraseña'] = contrasenia
                request.session['registro_data'] = datos_registro
            except UsuariosPermitidos.DoesNotExist:
                return JsonResponse({"success": False, "errors": "Acceso restringido. No estás autorizado."})

            # enviar mail con el codigo
            try:
                asunto = "Validación de cuenta - Fresh & Simple"
                mensaje_texto = f"Tu código de validación es: {permitido.codigo_validacion}\n\nPor favor, ingresa este código en el sitio para validar tu cuenta."
                cuerpoMensajeHtml = f"""
                    <html>
                        <body style="font-family: Arial, sans-serif; background-color: #F7F7F7; padding: 30px;">
                            <div style="max-width: 600px; margin: auto; background-color: #FFFFFF; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); border: 1px solid #e0e0e0;">
                                <h2 style="color: #2E8A99; text-align: center;">Validación de cuenta Fresh & Simple</h2>
                                <p style="font-size: 16px; color: #4A4A4A; text-align: center;">
                                    Hola {nombre}<br><br>
                                    Gracias por registrarte en Fresh & Simple.<br>
                                    Para activar tu cuenta, utiliza el siguiente código de validación:<br>
                                    <span style="display: inline-block; margin: 20px auto; padding: 15px 25px; font-size: 22px; font-weight: bold; color: #FF6363; border: 2px dashed #FF6363; border-radius: 8px;">{permitido.codigo_validacion}</span><br><br>
                                    Ingresa este código en el sitio para completar la validación de tu cuenta.<br><br>
                                    <a href="https://freshandsimple.onrender.com/validar/" 
                                       style="display: inline-block; background-color: #2E8A99; color: white; padding: 12px 25px; border-radius: 6px; text-decoration: none; font-weight: bold;">
                                        Ir a la página de validación
                                    </a><br><br>
                                    Si no solicitaste este registro, ignora este correo.<br><br>
                                    ¡Gracias por elegirnos!<br><br>
                                    <strong style="color: #FF6363;">Fresh & Simple</strong>
                                </p>
                                <p style="margin-top: 40px; font-size: 12px; text-align: center; color: #888888;">
                                    Este es un correo automático, por favor no respondas a este mensaje.
                                </p>
                            </div>
                        </body>
                    </html>
                """
                destinatario = email
                send_mail(
                    asunto,
                    mensaje_texto,
                    settings.EMAIL_HOST_USER,
                    [destinatario],
                    fail_silently=False,
                    html_message=cuerpoMensajeHtml
                )
                return JsonResponse({'success': True, 'message': "Te enviamos un código de verificación de cuenta. A continuación te redirigiremos a la página...", 'redirect_url': reverse('validar_registro')})
            except Exception as e:
                return JsonResponse({"success": False, "errors": f"Error al enviar correo: {e}"})
    else:
        form = RegistroForm()
    return render(request, 'tienda/registro.html', {'form': form})

#Vista validar registro
def validar_registro(request):
    datos = request.session.get('registro_data')
    # si no hay datos en la sesion denego el acceso
    if not datos:
        return HttpResponseForbidden("Acceso no autorizado.")

    # verifica si el email esta autorizado sino denego acceso
    if not UsuariosPermitidos.objects.filter(email=datos['email']).exists():
        return HttpResponseForbidden("Acceso no autorizado.")

    if request.method == 'POST':
        form = ValidarCodigoForm(request.POST)
        if form.is_valid():
            codigo = form.cleaned_data['codigo']

            if User.objects.filter(email__iexact=datos['email']).exists():
                return JsonResponse({'success': False, 'errors': "Ya hay una cuenta registrada con este email."})

            if not UsuariosPermitidos.objects.filter(email__iexact=datos['email'], codigo_validacion=codigo).exists():
                return JsonResponse({'success': False, 'errors': "Código inválido."})

            # Creo el usuario de Django
            user = User.objects.create_user(
                username=datos['email'],
                email=datos['email'],
                password=datos['contraseña'],
                first_name=datos['nombre'],
                last_name=datos['apellido'],
            )
            #Vacio los datos de sesion
            del request.session['registro_data']

            return JsonResponse({'success': True, 'message': "Cuenta validada. Ya podés iniciar sesión con tu email y contraseña. A continuación te redirigiremos a la página...",'redirect_url': reverse('login')})

    else:
        form = ValidarCodigoForm()
    return render(request, 'tienda/validar_registro.html', {'form': form})

#Vista para recuperar la contraseña
def recuperar_contraseña(request):
    if request.method == 'POST':
        form = RecuperarContraseñaForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            if not User.objects.filter(email__iexact=email).exists():
                return JsonResponse({'success': False, 'errors': "No hay ninguna cuenta registrada con este email."})
            else:
                datos_registro = form.cleaned_data.copy()
                request.session['registro_data'] = datos_registro
                usuario = User.objects.get(email__iexact=email)
                # enviar mail con el codigo
                try:
                    asunto = "Recuperación de cuenta - Fresh & Simple"
                    mensaje_texto = f"El enlace para cambiar tu contraseña es: https://freshandsimple.onrender.com/cambiar_contraseña/"
                    cuerpoMensajeHtml = f"""
                                   <html>
                                       <body style="font-family: Arial, sans-serif; background-color: #F7F7F7; padding: 30px;">
                                           <div style="max-width: 600px; margin: auto; background-color: #FFFFFF; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); border: 1px solid #e0e0e0;">
                                               <h2 style="color: #2E8A99; text-align: center;">Recuperar contraseña. Fresh & Simple</h2>
                                               <p style="font-size: 16px; color: #4A4A4A; text-align: center;">
                                                   Hola {usuario.first_name}!<br><br>
                                                   Para recuperar tu cuenta ingresá al siguiente enlace:<br><br>
                                                   <a href="https://freshandsimple.onrender.com/cambiar_contraseña/" 
                                                      style="display: inline-block; background-color: #2E8A99; color: white; padding: 12px 25px; border-radius: 6px; text-decoration: none; font-weight: bold;">
                                                      Cambiar Contraseña
                                                   </a><br><br>
                                                   Si no fuiste vos, contactanos.<br><br>
                                                   <strong style="color: #FF6363;">Fresh & Simple</strong>
                                               </p>
                                               <p style="margin-top: 40px; font-size: 12px; text-align: center; color: #888888;">
                                                   Este es un correo automático, por favor no respondas a este mensaje.
                                               </p>
                                           </div>
                                       </body>
                                   </html>
                               """
                    destinatario = email
                    send_mail(
                        asunto,
                        mensaje_texto,
                        settings.EMAIL_HOST_USER,
                        [destinatario],
                        fail_silently=False,
                        html_message=cuerpoMensajeHtml
                    )
                    return JsonResponse({'success': True, 'message': f"Te enviamos los pasos para cambiar tu contraseña al email {email}."})
                except Exception as e:
                    return JsonResponse({"success": False, "errors": f"Error al enviar correo: {e}"})
    else:
        form = RecuperarContraseñaForm()
    return render(request, 'tienda/recuperar_cuenta.html', {'form': form})

#Vista para recuperar la contraseña
def cambiar_contrasenia(request):
    #Si el usuario esta logeado y quiere cambiar su contraseña
    if request.user.is_authenticated:
        email = request.user.email #Si es desde la sesion lo guardo
        esRecuperacion = False
    else:
        # si no hay datos en la sesion denego el acceso (Es decir no selecciono Olvide mi contraseña)
        datos = request.session.get('registro_data')
        if not datos:
            return HttpResponseForbidden("Acceso no autorizado.")
        email = datos.get('email') # Si es desde la recuperacion lo guardo
        esRecuperacion = True

    # verifica si el email esta autorizado sino denego acceso
    if not UsuariosPermitidos.objects.filter(email=email).exists():
        return HttpResponseForbidden("Acceso no autorizado.")

    if request.method == 'POST':
        form = CambiarContraseñaForm(request.POST)
        if form.is_valid():
            contrasenia = form.cleaned_data['contraseña']
            confirmarContrasenia = form.cleaned_data['confirmar_contraseña']

            if not User.objects.filter(email__iexact=email).exists():
                return JsonResponse({'success': False, 'errors': "No hay ninguna cuenta registrada con este email."})
            else:
                if contrasenia != confirmarContrasenia:
                    return JsonResponse({'success': False, 'errors': "Las contraseñas no coinciden."})
                else:
                    usuario = User.objects.get(email__iexact = email)
                    usuario.set_password(contrasenia)
                    usuario.save()
                    # Si uso recuperacion, vacio los datos de sesion
                    if esRecuperacion and 'registro_data' in request.session:
                        del request.session['registro_data']
                    return JsonResponse({'success': True, 'message': "Cambiaste tu contraseña con éxito. A continuación te redirigiremos al login...",'redirect_url': reverse('login')})
    else:
        form = CambiarContraseñaForm()
    return render(request, 'tienda/cambiar_contrasenia.html', {'form': form})


#Vista Dashboard
@login_required()
def dashboard (request):
    return render(request, 'tienda/dashboard.html', {'consultas': consultas})

#vista Consultas
@login_required()
def consultas(request):
    consultas = Consultas.objects.all()
    contadorConsultasTotal = 0
    contadorConsultasComerciales = 0
    contadorConsultasTecnicas = 0
    contadorConsultasRrhh = 0
    contadorConsultasGenerales = 0
    for consulta in consultas:
        categoria = consulta.categoria_detectada.lower()
        contadorConsultasTotal+=1
        match categoria:
            case "consulta comercial":
                contadorConsultasComerciales+=1
            case "consulta técnica":
                contadorConsultasTecnicas+=1
            case "consulta de rrhh":
                contadorConsultasRrhh+=1
            case _:
                contadorConsultasGenerales+=1
    return render(request, 'tienda/consultas.html', {'consultas': consultas, 'totalConsultas': contadorConsultasTotal, 'consultasComerciales': contadorConsultasComerciales, 'consultasTecnicas': contadorConsultasTecnicas, 'consultasRRHH' : contadorConsultasRrhh, 'consultasGenerales' :contadorConsultasGenerales})

#Vista Productos
@login_required()
def productos(request):
    tipo_filtro = request.GET.get('tipo', '')
    productos = Productos.objects.all()
    if tipo_filtro:
        productos = productos.filter(tipo=tipo_filtro)

    return render(request, 'tienda/productos.html', {'productos': productos, 'tipo_filtro': tipo_filtro})

#Vista registrar producto
@login_required()
def registrar_producto(request):
    if request.method == "POST":  # Si el metodo de respuesta es post
        form = ProductoForm(request.POST, request.FILES)
        #Verifico si el form es valido
        if form.is_valid():
            imagen = request.FILES.get('imagen')
            # Validaciones manuales en la vista
            if imagen:
                if imagen.size > 1 * 1024 * 1024:
                    return JsonResponse(
                        {"success": False, "errors": "La imagen no puede pesar más de 1 MB."})
                if imagen.content_type not in ["image/webp"]:
                    return JsonResponse({"success": False, "errors": "Solo se permiten imágenes WEBP."})

            #Obtengo los datos del formulario
            nombre = form.cleaned_data["nombre"]
            precio = form.cleaned_data["precio"]
            tipo = form.cleaned_data["tipo"]

            #Guardo en la DB
            producto = Productos(
                nombre = nombre,
                precio = precio,
                tipo = tipo,
                imagen = imagen
            )
            producto.save()

            return JsonResponse({"success": True,
                                 "message": f"Se registró con éxito el producto {nombre}"})
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
        form = ProductoForm(request.POST)
        form.fields['imagen'].required = False
        if form.is_valid():
            #obtengo los valores (antiguos) del formulario
            nombreAntiguo = producto.nombre
            precioAntiguo = producto.precio

            # obtengo los datos del formulario que puede cambiar (actuales)
            producto.nombre = form.cleaned_data["nombre"]
            producto.precio = form.cleaned_data["precio"]

            if producto.nombre == nombreAntiguo and producto.precio == precioAntiguo:
                return JsonResponse({"success": False, "errors": "No realizaste modificaciones."})
            else:
                # actualizo los valores de la consulta
                producto.save()
            return JsonResponse({"success": True, "message": "Producto modificado con éxito."})
        else:
            return JsonResponse({"success": False, "errors": form.errors}, status=400)

    else:
        #lleno el formulario con los datos actuales del producto
        form = ProductoForm(initial={
            'nombre': producto.nombre,
            'precio': producto.precio,
            'tipo': producto.tipo,
            'imagen': producto.imagen
        })

        #Le pongo al campo tipo un atributo readonly para evitar su modificacion
        form.fields["tipo"].widget.attrs['readonly'] = True

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
            emailAntiguo = consulta.email
            telefonoAntiguo = consulta.telefono

            # obtengo los datos del formulario que puede cambiar (actuales)
            consulta.email = form.cleaned_data["email"]
            consulta.telefono = form.cleaned_data["telefono"]

            if consulta.email == emailAntiguo and consulta.telefono == telefonoAntiguo:
                return JsonResponse({"success": False, "errors": "No realizaste modificaciones."})
            else:
                # actualizo los valores de la consulta
                consulta.save()
            return JsonResponse({"success": True, "message": "Consulta modificada con éxito."})
        else:
            return JsonResponse({"success": False, "errors": form.errors}, status=400)

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
    contadorConsultasTotal = Consultas.objects.count()
    contadorConsultasComerciales = Consultas.objects.filter(categoria_detectada="Consulta Comercial").count()
    contadorConsultasTecnicas = Consultas.objects.filter(categoria_detectada="Consulta Técnica").count()
    contadorConsultasRrhh = Consultas.objects.filter(categoria_detectada="Consulta de RRHH").count()
    contadorConsultasGenerales = Consultas.objects.filter(categoria_detectada="Consulta General").count()

    return JsonResponse({"success": True, 'totalConsultas': contadorConsultasTotal, 'consultasComerciales': contadorConsultasComerciales, 'consultasTecnicas': contadorConsultasTecnicas, 'consultasRRHH' : contadorConsultasRrhh, 'consultasGenerales' :contadorConsultasGenerales})

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

# clase para el viewSet de Consultas
class ConsultasViewSet(viewsets.ModelViewSet):
    queryset =  Consultas.objects.all()
    serializer_class = ConsultasSerializer
    permission_classes = [IsAuthenticated] #Protejo los endpoint, si no esta logeado desde dashboard no puede acceder en un futuro se usara JWT

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

class CustomLoginView(LoginView):
    template_name = 'tienda/login.html'
    authentication_form = AuthenticationForm  # puede ser AuthenticationForm también
    success_url = reverse_lazy('home')  # ajusta según tu app

    def post(self, request, *args, **kwargs):
        email = request.POST.get('username')  # por defecto LoginView usa 'username'

        if '@' in email and not User.objects.filter(email=email).exists():
            messages.error(request, "Este correo no está registrado. Puedes crear una cuenta.")
            return redirect('registro')  # o vuelve a login con error

        return super().post(request, *args, **kwargs)