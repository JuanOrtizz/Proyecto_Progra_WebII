import {generarAlertError} from './alertas.js' // importo la alerta
import {validarFormulario} from './validacionesFormProductos.js' // Importo las validaciones

document.addEventListener('DOMContentLoaded', ()=>{

    // capturo el formulario y el token
    const formularioModificarProducto = document.getElementById("form_modificar_producto")
    const csrfToken = document.querySelector('[name = csrfmiddlewaretoken]').value

    // Evento para evitar que se mande el form
    if(formularioModificarProducto){
            formularioModificarProducto.addEventListener('submit', (e) =>{
                // evita recargar la pagina al mandar el formulario
                e.preventDefault()
                // captura los datos del formulario
                let formData = new FormData(formularioModificarProducto)
                // valida los campos
                if(validarFormulario(formData)){
                    Swal.fire({ // Muestra alerta
                        title: "¿Estás seguro que querés modificar este producto?",
                        text: "No podrás revertir esto",
                        icon: "warning",
                        showCancelButton: true,
                        confirmButtonColor: "#3085d6",
                        cancelButtonColor: "#d33",
                        confirmButtonText: "Sí Modificar",
                        didOpen: () =>{ // agrego esto ya que sino recalcula con esta clase y sube el footer para evitar scroll
                            document.body.classList.remove('swal2-height-auto')
                            document.body.style.overflow = 'auto'
                            document.body.style.paddingRight = '0'
                        }
                    }).then((result) => {
                        if (result.isConfirmed) { // si confirma envia el formulario y modifica el producto
                            enviarFormulario(formData, csrfToken)
                        }
                    })
                }
            })
    }

})

// funcion async para utilizar await y manejar asincronia
async function enviarFormulario(formData, csrfToken){
    // hago fetch del formulario
    try
    {
        const response = await fetch("",{
            method:"POST",
            body: formData,
            headers:{
                "X-CSRFToken": csrfToken
            }
        })
        const data = await response.json()
        if(data.success){
            // guarda en el sessionStorage el mensaje de exito para mostrar en productos.html
            sessionStorage.setItem('mensajeExito', data.message)
            window.location.href = "/dashboard/productos/" //redirige a productos.html
        }else{
            if(data.errors){
                console.log("Se recibieron errores:", data.errors)

                generarAlertError(data.errors)
            }
            else{
                generarAlertError("Ocurrió un error al modificar el producto. Intenta nuevamente.")
            }
        }
    }catch(error){
        console.error("Error en la modificación: ", error)
        generarAlertError("Error al modificar el producto. Intentá más tarde.")
    }
}