import {validarFormulario} from './validacionesFormContacto.js'
import {generarAlertExito, generarAlertError} from './alertas.js'

document.addEventListener('DOMContentLoaded', ()=>{
    // capturo el formulario y el token
    const formularioContacto = document.getElementById("form_contacto")
    const csrfToken = document.querySelector('[name = csrfmiddlewaretoken]').value

    // Evento para evitar que se mande el form
    formularioContacto.addEventListener('submit', (e) =>{
            // evita recargar la pagina al mandar el formulario
            e.preventDefault()
            // captura los datos del formulario
            const formData = new FormData(formularioContacto)
            // valida los campos
            if(validarFormulario(formData)){
                enviarFormulario(formData, csrfToken, formularioContacto)
            }
        })
})

// funcion async para utilizar await y manejar asincronia
async function enviarFormulario(formData, csrfToken, formularioContacto){
    const overlay = document.getElementById("pantalla_carga") // Obtiene el overlay (pantalla de carga)
    overlay.style.display = "flex" // Muestra el overlay (pantalla de carga)
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
            generarAlertExito(data.message)
            // vacio el formulario
            formularioContacto.reset()
        }else{
            generarAlertError(data.errors)
        }
    }catch(error){
        console.error("Error en la Consulta: ", error)
        generarAlertError("Ocurrió un error inesperado. Intentá más tarde.")
    }finally {
        overlay.style.display = "none" // oculta el overlay (pantalla de carga)
    }
}