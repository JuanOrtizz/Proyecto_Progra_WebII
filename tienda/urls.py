from django.urls import path, include, re_path
from . import views
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from .views import ConsultasViewSet, ProductosViewSet, ObtenerFraseAPIView, CustomPasswordResetView, CustomPasswordResetConfirmView, CustomPasswordChangeView, MediaServeView, CustomLoginView


#declaro el router y los endpoints para Consultas y Productos
router = DefaultRouter()
router.register(r'Consultas', ConsultasViewSet)
router.register(r'Productos', ProductosViewSet)

urlpatterns = [
    path('', views.pagina_index, name='index'), # path para el index
    path('colecciones/', views.colecciones, name="colecciones"), #path para el formulario de contacto
    path('locales/', views.locales, name='locales'), #path para los locales
    path('contacto/', views.contacto, name="contacto"), #path para el formulario de contacto
    path('coleccion/<str:tipo>/', views.coleccion_filtrada, name='coleccion-filtrada'), #path para las colecciones filtradas (Por ejemplo buzos)
    path('coleccion/<str:tipo>/<int:producto_id>', views.producto_detalles, name='producto-detalles'), #path para los detalles del producto
    path('login/', CustomLoginView.as_view(), name='login'),  # path para el login
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # path para el logout
    path('registro/', views.registro, name="registro"), #path para el registro
    path('validar-registro/', views.validar_registro, name="validar-registro"), #path para validar el registro
    path('recuperar-cuenta/', CustomPasswordResetView.as_view(), name='recuperar-cuenta'), #path para recuperar la cuenta desde "Olvidé mi contraseña"
    path('cambiar-contrasenia/', CustomPasswordChangeView.as_view(), name='cambiar-contrasenia'), #path para cambiar la contraseña si esta logeado
    path('recuperar-contrasenia/confirmar/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='recuperar-contrasenia-confirmar'), # path para cambiar la constraseña si no esta logeado (Olvide mi contraseña), se obtiene por mail
    path('dashboard/', views.dashboard, name='dashboard'),  # path para el dashboard
    path('dashboard/consultas/', views.consultas, name='consultas'),#path para las consultas desde el dashboard
    path('dashboard/productos/', views.productos, name='productos'), #path para los productos desde el dashboard
    path('dashboard/consultas/modificar-consulta/<int:consulta_id>/', views.modificar_consulta, name='modificar-consulta'),# path para modificar consultas
    path('dashboard/consultas/eliminar-consulta/<int:consulta_id>/', views.eliminar_consulta, name='eliminar-consulta'),# path para eliminar consultas
    path('dashboard/productos/registrar-producto/', views.registrar_producto, name='registrar-producto'),# path para agregar un producto
    path('dashboard/productos/modificar-producto/<int:producto_id>/', views.modificar_producto, name='modificar-producto'),# path para modificar productos
    path('dashboard/productos/eliminar-producto/<int:producto_id>/', views.eliminar_producto, name='eliminar-producto'),# path para eliminar productos
    path('obtener-frase/', ObtenerFraseAPIView.as_view(), name='obtener-frase'),  # agrego esta ruta para la API externa
    path('api/', include(router.urls)), #path para exponer los endpoints con el router
    re_path(r'^media/(?P<path>.*)$', MediaServeView.as_view(), name='media'), #re_path para servir archivos media en produccion con DEBUG =FALSE
]