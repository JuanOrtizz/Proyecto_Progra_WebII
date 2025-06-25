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
                    enviarFormulario(formData, csrfToken)
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
        console.log("hola")
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
                generarAlertError("Ocurrió un error al modificar el producto. Intenta nuevamente")
            }
        }
    }catch(error){
        console.error("Error en la modificación: ", error)
        generarAlertError("Error al modificar el producto. Intenta mas tarde")
    }
}