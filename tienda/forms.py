from django import forms
from django.forms import CharField, Select

# Formulario de contacto en contacto.html
class ContactoForm(forms.Form):
    nombre = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Nombre y Apellido', 'id': 'nombre'}),
        max_length=100,
        required=True
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email', 'id': 'email'}),
        max_length=320,
        required=True,
    )

    telefono = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Teléfono', 'id': 'telefono' }),
        max_length=25,
        required=True
    )

    mensaje = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Coloca tu mensaje aquí...', 'id': 'mensaje'})
    )


class ProductoForm(forms.Form):
    nombre = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Nombre del producto', 'id': 'nombre'}),
        max_length=100,
        required=True
    )

    precio = forms.DecimalField(
        widget=forms.NumberInput(attrs={'placeholder': 'Precio', 'id': 'precio'}),
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

# Formulario para el registro
class RegistroForm(forms.Form):
    nombre = forms.CharField(
        max_length=100,
        widget = forms.TextInput(attrs={'placeholder': 'Nombre', 'id': 'nombre'}),
    )
    apellido = forms.CharField(
        max_length=100,
        widget = forms.TextInput(attrs={'placeholder': 'Apellido', 'id': 'apellido'}),
    )
    email = forms.EmailField(
        max_length=320,
        widget = forms.EmailInput(attrs={'placeholder': 'Email', 'id': 'email'}),
    )
    contraseña = forms.CharField( max_length=20, widget=forms.PasswordInput(attrs={'placeholder' : 'Contraseña', 'id' : 'contraseña'}))

# Formulario para validar el registro con el codigo
class ValidarCodigoForm(forms.Form):
    codigo = forms.CharField(max_length=6,widget = forms.TextInput(attrs={'placeholder': 'Colocá el código acá', 'id': 'código'}),)

# Formulario para el registro
class RecuperarContraseñaForm(forms.Form):
    email = forms.EmailField(
        max_length=320,
        widget = forms.EmailInput(attrs={'placeholder': 'Email', 'id': 'email'}),
    )

# Formulario para el registro
class CambiarContraseñaForm(forms.Form):
    contraseña = forms.CharField( max_length=20, widget=forms.PasswordInput(attrs={'placeholder' : 'Contraseña', 'id' : 'contraseña'}))
    confirmar_contraseña = forms.CharField( max_length=20, widget=forms.PasswordInput(attrs={'placeholder' : 'Confirmar contraseña', 'id' : 'confirmar_contraseña'}))
