import {generarAlertExito} from './alertas.js' //importo la alerta
let productoIdAEliminar = null // declaro el id de la consulta a eliminar

document.addEventListener('DOMContentLoaded', ()=>{
    // Bloque de codigo para mostrar Mensaje de exito al modificar el producto.
    // obtiene desde el sessionStorage el mensaje de exito
    const mensajeAlert = sessionStorage.getItem('mensajeExito')
    if(mensajeAlert){ // Si mensaje de exito existe y no es null
        generarAlertExito(mensajeAlert) // Muestra la alerta de Consulta modificada con exito
        sessionStorage.removeItem('mensajeExito') // Elimina el par clave-valor del sessionStorage
    }

    const botonesEliminar = document.querySelectorAll('.boton_eliminar') // obtengo todos los botones eliminar de la tabla
    // recorro cada uno de esos botones y les pongo un eventListener
    botonesEliminar.forEach(boton => {
        boton.addEventListener('click', () =>{
            productoIdAEliminar = boton.getAttribute('data-id') // Obtiene el data-id (Producto)
            if(productoIdAEliminar){
                Swal.fire({ // Muestra alerta
                    title: "¿Estás seguro que querés eliminar este producto?",
                    text: "No podrás revertir esto",
                    icon: "warning",
                    showCancelButton: true,
                    confirmButtonColor: "#3085d6",
                    cancelButtonColor: "#d33",
                    confirmButtonText: "Sí Eliminar",
                    didOpen: () =>{ // agrego esto ya que sino recalcula con esta clase y sube el footer para evitar scroll
                        document.body.classList.remove('swal2-height-auto')
                        document.body.style.overflow = 'auto'
                        document.body.style.paddingRight = '0'
                    }
                }).then((result) => {
                    if (result.isConfirmed) { // si confirma hace un fetch y elimina el producto con ese id
                        const overlay = document.getElementById("pantalla_carga") // Obtiene el overlay (pantalla de carga)
                        overlay.style.display = "flex" // Muestra el overlay (pantalla de carga)
                        fetch(`/dashboard/productos/eliminar-producto/${productoIdAEliminar}/`,{
                        method: 'GET',
                        headers: {
                            'X-Requested-With': 'XMLHttpRequest'
                        }
                        })
                        .then(response => response.json())
                        .then(data =>{
                            const row = document.getElementById(`producto-${productoIdAEliminar}`)
                            if(row){
                                row.remove() // elimina de la tabla
                                generarAlertExito("Se ha eliminado con éxito.") // muestra alerta
                            }
                        })
                        .catch(error =>{
                            console.error("Error al eliminar:", error)
                        })
                        .finally(() =>{
                                overlay.style.display = "none" // oculta el overlay (pantalla de carga)
                            }
                        )
                    }
                })
            }
        })
    })
})