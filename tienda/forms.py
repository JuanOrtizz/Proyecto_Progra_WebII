import re
from decimal import Decimal
from django import forms
from django.forms import Select

# Formulario de contacto en contacto.html
class ContactoForm(forms.Form):
    nombre = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Nombre y Apellido', 'id': 'id_nombre'}),
        max_length=100,
        required=True
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email', 'id': 'id_email'}),
        max_length=254,
        required=True,
    )

    telefono = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Teléfono', 'id': 'id_telefono' }),
        max_length=25,
        required=True
    )

    mensaje = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Coloca tu mensaje aquí...', 'id': 'id_mensaje'})
    )

    #Validaciones del formulario
    #Validacion de nombre
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '').strip()
        #Verifica si la longitud del nombre esta entre 2 y 100 caracteres
        if len(nombre) >= 2 and len(nombre) <= 100:
            #Verifica que sea un nombre valido
            if not re.match(r'^[a-záéíóúñ]+(?:\s[a-záéíóúñ]+)*$', nombre, re.IGNORECASE):
                raise forms.ValidationError("El nombre no es válido (solo letras y espacios).")
        else:#Si la longitud no es valida devuelve este error
            raise forms.ValidationError("Nombre: de 2 a 100 caracteres")
        #Retorno el nombre si es valido
        return nombre

    #Validacion de email
    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip()
        if len(email) >= 6 and len(email) <= 254:
            if not re.match('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email, re.IGNORECASE):
                raise forms.ValidationError("El email no es válido.")
        else:
            raise forms.ValidationError("Email: de 6 a 254 caracteres.")
        return email

    #Validacion del telefono
    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono', '').strip()
        if len(telefono) >= 6 and len(telefono) <= 25:
            if not re.match(r'^\+?[0-9]{6,25}$', telefono):
                raise forms.ValidationError("El celular no es válido.")
        else:
            raise forms.ValidationError("Celular: de 6 a 25 caracteres.")
        return telefono

    #Validacion de mensaje
    def clean_mensaje(self):
        mensaje =self.cleaned_data.get('mensaje', '').strip()
        if len(mensaje) < 2 or len(mensaje) > 1000:
            raise forms.ValidationError("Mensaje: de 2 a 1000 caracteres.")
        return mensaje

#Formulario de producto (Insert y Update)
class ProductoForm(forms.Form):
    nombre = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Nombre del producto', 'id': 'id_nombre'}),
        max_length=100,
        required=True
    )

    precio = forms.DecimalField(
        widget=forms.NumberInput(attrs={'placeholder': 'Precio', 'id': 'id_precio'}),
        max_digits=10,
        decimal_places=2,
        required=True,
    )

    tipo = forms.ChoiceField(
        choices=[
            ('', 'Selecciona una opción'),
            ('1', 'Pantalon'),
            ('2', 'Remera'),
            ('3', 'Top'),
            ('4', 'Vestido'),
            ('5', 'Buzo'),
            ('6', 'Campera'),
            ('7', 'Accesorio')
        ],
        widget=Select(attrs={'id': 'tipo'}),
    )

    imagen = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={
            'placeholder': 'Carga la imagen del producto',
            'id': 'imagen',
            'class': 'input_file',
            'accept': '.webp'
        })
    )

    #Validaciones del formulario
    #Validacion al iniciar el form
    def __init__(self, *args, **kwargs):
        self.imagen_actual = kwargs.pop('imagen_actual', None) # extraigo la imagen actual del producto desde la vista
        super().__init__(*args, **kwargs)

    #Validacion nombre producto
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '').strip()
        #Verifica si la longitud del nombre del producto esta entre 2 y 100 caracteres
        if len(nombre) >= 2 and len(nombre) <= 100:
            #Verifica que sea un nombre valido
            if not re.match(r'^[a-záéíóúñ0-9]+(?:\s[a-záéíóúñ0-9]+)*$', nombre, re.IGNORECASE):
                raise forms.ValidationError("El nombre no es válido.")
        else:#Si la longitud no es valida devuelve este error
            raise forms.ValidationError("Nombre: de 2 a 100 caracteres")
        #Retorno el nombre si es valido
        return nombre

    #validacion precio
    def clean_precio(self):
        precio = self.cleaned_data.get('precio', '')
        if precio < Decimal('1.00'):
            raise forms.ValidationError("Precio mínimo: $1")
        elif precio > Decimal('9999999.99'):
            raise forms.ValidationError("Precio máximo: $9.999.999,99")

        if abs(precio.as_tuple().exponent) > 2:
            raise forms.ValidationError("El precio no es válido (Máximo 2 decimales)")
        return precio

    #validacion tipo producto
    def clean_tipo(self):
        tipo = self.cleaned_data.get('tipo','')
        if not tipo:
            raise forms.ValidationError("El campo está vacío")
        return tipo

    #validacion imagen
    def clean_imagen(self):
        imagen = self.cleaned_data.get('imagen')

        if not imagen:
            # Si no hay imagen subida y no hay archivos, es error (creación)
            if not self.imagen_actual:
                raise forms.ValidationError("El producto debe tener una imagen")
            # Si no hay imagen y hay archivos, pero el archivo no es imagen, dará error en otro lado
            return self.imagen_actual

        # Valido tipo
        if imagen.content_type != 'image/webp':
            raise forms.ValidationError("La imagen debe ser en formato WEBP")

        # Valido tamaño
        max_tamano_mb = 1
        if imagen.size > max_tamano_mb * 1024 * 1024:
            raise forms.ValidationError(f"La imagen no puede superar los {max_tamano_mb} MB")

        return imagen

# Formulario para el registro de usuario
class RegistroForm(forms.Form):
    nombre = forms.CharField(
        max_length=100,
        widget = forms.TextInput(attrs={'placeholder': 'Nombre', 'id': 'id_nombre'}),
    )
    apellido = forms.CharField(
        max_length=100,
        widget = forms.TextInput(attrs={'placeholder': 'Apellido', 'id': 'id_apellido'}),
    )
    email = forms.EmailField(
        max_length=320,
        widget = forms.EmailInput(attrs={'placeholder': 'Email', 'id': 'id_email'}),
    )
    contrasenia = forms.CharField( max_length=20, widget=forms.PasswordInput(attrs={'placeholder' : 'Contraseña', 'id' : 'id_contrasenia'}))

    #Validaciones del formulario
    #Validacion de nombre
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '').strip()
        #Verifica si la longitud del nombre esta entre 2 y 100 caracteres
        if len(nombre) >= 2 and len(nombre) <= 100:
            #Verifica que sea un nombre valido
            if not re.match(r'^[a-záéíóúñ]+(?:\s[a-záéíóúñ]+)*$', nombre, re.IGNORECASE):
                raise forms.ValidationError("El nombre no es válido (solo letras y espacios).")
        else:#Si la longitud no es valida devuelve este error
            raise forms.ValidationError("Nombre: de 2 a 100 caracteres")
        #Retorno el nombre si es valido
        return nombre

    #Validacion de apellido
    def clean_apellido(self):
        apellido = self.cleaned_data.get('apellido', '').strip()
        #Verifica si la longitud del apellido esta entre 2 y 100 caracteres
        if len(apellido) >= 2 and len(apellido) <= 100:
            #Verifica que sea un apellido valido
            if not re.match(r'^[a-záéíóúñ]+(?:\s[a-záéíóúñ]+)*$', apellido, re.IGNORECASE):
                raise forms.ValidationError("El apellido no es válido (solo letras y espacios).")
        else:#Si la longitud no es valida devuelve este error
            raise forms.ValidationError("Apellido: de 2 a 100 caracteres")
        #Retorno el nombre si es valido
        return apellido

    # Validacion de email
    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip()
        if len(email) >= 6 and len(email) <= 254:
            if not re.match('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email, re.IGNORECASE):
                raise forms.ValidationError("El email no es válido.")
        else:
            raise forms.ValidationError("Email: de 6 a 254 caracteres.")
        return email

    def clean_contrasenia(self):
        contrasenia = self.cleaned_data.get('contrasenia', '').strip()
        if len(contrasenia) >= 8 and len(contrasenia) <= 20:
            if not re.match('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$', contrasenia):
                raise forms.ValidationError("La contraseña debe contener mayúsculas, minúsculas y números")
        else:
            raise forms.ValidationError("Contraseña: de 8 a 20 caracteres")
        return contrasenia

# Formulario para validar el registro con el codigo
class ValidarCodigoForm(forms.Form):
    codigo = forms.CharField(max_length=6,widget = forms.TextInput(attrs={'placeholder': 'Colocá el código acá', 'id': 'id_codigo'}),)

    def clean_codigo(self):
        codigo = self.cleaned_data.get('codigo','').strip()
        if len(codigo) != 6:
            raise forms.ValidationError("El código debe tener 6 dígitos")
        return codigo