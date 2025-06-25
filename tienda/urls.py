from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from .views import ConsultasViewSet, ProductosViewSet
from django.conf import settings
from django.conf.urls.static import static

#declaro el router y los endpoints para Consultas y Productos
router = DefaultRouter()
router.register(r'Consultas', ConsultasViewSet)
router.register(r'Productos', ProductosViewSet)

urlpatterns = [
    path('', views.pagina_index, name='index'), # path para el index
    path('colecciones/', views.colecciones, name="colecciones"), #path para el formulario de contacto
    path('locales/', views.locales, name='locales'), #path para los locales
    path('contacto/', views.contacto, name="contacto"), #path para el formulario de contacto
    path('coleccion/<str:tipo>/', views.coleccion_filtrada, name='coleccion_filtrada'), #path para las colecciones filtradas (Por ejemplo buzos)
    path('login/', auth_views.LoginView.as_view(template_name='tienda/login.html'), name='login'),  # path para el login
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # path para el logout
    path('registro/', views.registro, name="registro"), #path para el registro
    path('validar/', views.validar_registro, name="validar_registro"), #path para validar el registro
    path('dashboard/', views.dashboard, name='dashboard'),  # path para el dashboard
    path('dashboard/consultas/', views.consultas, name='consultas'),#path para las consultas desde el dashboard
    path('dashboard/productos/', views.productos, name='productos'), #path para los productos desde el dashboard
    path('dashboard/productos/agregarProducto/', views.registrar_producto, name='agregar_producto'), #path para agregar un producto
    path('dashboard/consultas/modificarConsulta/<int:consulta_id>/', views.modificar_consulta, name='modificar_consulta'),# path para modificar consultas
    path('dashboard/consultas/eliminarConsulta/<int:consulta_id>/', views.eliminar_consulta, name='eliminar_consulta'),# path para eliminar consultas
    path('dashboard/productos/modificarProducto/<int:producto_id>/', views.modificar_producto, name='modificar_producto'),# path para modificar productos
    path('dashboard/productos/eliminarProducto/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),# path para eliminar productos
    path('obtener-frase/', views.obtener_frase, name='obtener_frase'),  # agrego esta ruta para la API externa
    path('api/', include(router.urls)), #path para exponer los endpoints con el router
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

