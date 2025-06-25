import {validarFormulario} from './validacionesFormRegistro.js'
import {generarAlertExito, generarAlertError} from './alertas.js'

document.addEventListener('DOMContentLoaded', ()=>{
    // capturo el formulario y el token
    const formularioValidarRegistro = document.getElementById("form_login")
    const csrfToken = document.querySelector('[name = csrfmiddlewaretoken]').value

    // Evento para evitar que se mande el form
    formularioValidarRegistro.addEventListener('submit', (e) =>{
            // evita recargar la pagina al mandar el formulario
            e.preventDefault()
            // captura los datos del formulario
            const formData = new FormData(formularioValidarRegistro)
            // valida los campos
            if(validarFormulario(formData)){
                enviarFormulario(formData, csrfToken, formularioValidarRegistro)
            }
        })
})

// funcion async para utilizar await y manejar asincronia
async function enviarFormulario(formData, csrfToken, formularioValidarRegistro){
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
            formularioValidarRegistro.reset()
            //redirecciono despues de 4 segundos al html para iniciar sesion
            setTimeout(() => {
                window.location.href = data.redirect_url
            }, 4000)
        }else{
            formularioValidarRegistro.reset()
            generarAlertError(data.errors)
        }
    }catch(error){
        console.error("Error en La validación: ", error)
        generarAlertError("Ocurrió un error inesperado, intenta de nuevo mas tarde.")
    }finally {
        overlay.style.display = "none" // oculta el overlay (pantalla de carga)
    }
}