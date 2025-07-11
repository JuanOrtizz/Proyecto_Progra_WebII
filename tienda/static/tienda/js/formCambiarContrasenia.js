import {validarFormulario} from './validacionesFormsContrasenia.js'
import {generarAlertExito, generarAlertError} from './alertas.js'

document.addEventListener('DOMContentLoaded', ()=>{
    // capturo el formulario y el token
    const formularioCambiarContraseña = document.getElementById("form_recuperacion")
    const csrfToken = document.querySelector('[name = csrfmiddlewaretoken]').value

    // Evento para evitar que se mande el form
    formularioCambiarContraseña.addEventListener('submit', (e) =>{
            // evita recargar la pagina al mandar el formulario
            e.preventDefault()
            // captura los datos del formulario
            const formData = new FormData(formularioCambiarContraseña)
            // valida los campos
            if(validarFormulario(formData)){
                enviarFormulario(formData, csrfToken, formularioCambiarContraseña)
            }
        })
})

// funcion async para utilizar await y manejar asincronia
async function enviarFormulario(formData, csrfToken, formularioCambiarContraseña){
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
            formularioCambiarContraseña.reset()
            //redirecciono despues de 4 segundos al html para iniciar sesion
            setTimeout(() => {
                window.location.href = data.redirect_url
            }, 2000)
        }else{
            formularioCambiarContraseña.reset()
            generarAlertError(data.errors)
        }
    }catch(error){
        console.error("Error al cambiar la contraseña: ", error)
        generarAlertError("Ocurrió un error inesperado. Intentá más tarde.")
    }finally {
        overlay.style.display = "none" // oculta el overlay (pantalla de carga)
    }
}