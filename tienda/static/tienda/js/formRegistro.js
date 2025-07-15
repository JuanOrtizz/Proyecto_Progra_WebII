import {validarFormulario} from './validacionesFormRegistro.js'
import {generarAlertExito, generarAlertError} from './alertas.js'
import {textoErrorInput, eliminarErrorInput} from './erroresInputs.js'

document.addEventListener('DOMContentLoaded', ()=>{
    // capturo el formulario y el token
    const formularioRegistro = document.getElementById("form_login")
    const csrfToken = document.querySelector('[name = csrfmiddlewaretoken]').value

    // Evento para evitar que se mande el form
    formularioRegistro.addEventListener('submit', (e) =>{
        // evita recargar la pagina al mandar el formulario
        e.preventDefault()
        // captura los datos del formulario
        const formData = new FormData(formularioRegistro)
        // valida los campos
        if(validarFormulario(formData)){
            enviarFormulario(formData, csrfToken, formularioRegistro)
        }
    })
})

// funcion async para utilizar await y manejar asincronia
async function enviarFormulario(formData, csrfToken, formularioRegistro){
    const overlay = document.getElementById("pantalla_carga") // Obtiene el overlay (pantalla de carga)
    overlay.style.display = "flex" // Muestra el overlay (pantalla de carga)
    // hago fetch del formulario
    try
    {
        const response = await fetch("/registro/",{
            method:"POST",
            body: formData,
            headers:{
                "X-CSRFToken": csrfToken
            }
        })

        const data = await response.json()
        if(data.success){
            generarAlertExito(data.message)
            formularioRegistro.reset()
            //redirecciono despues de 4 segundos al html para validar la cuenta
            setTimeout(() => {
                window.location.href = data.redirect_url
            }, 4000)
        }else{
            const errores = data.errors //capturo los errores
            //Si los errores son string (provenientes de la vista)
            if (typeof errores === "string") {
                generarAlertError(data.errors)//Muestro una alerta
            }
            else{ // Sino (errores en formulario), muestro mediante un for estos errores provenientes de forms.py
                for (let campo in errores) {
                    const mensaje = errores[campo][0]
                    const input = document.getElementById(campo)
                    if (input) {
                        textoErrorInput(input, mensaje)
                    }
                }
            }
        }
    }catch(error){
        console.error("Error en el registro: ", error)
        generarAlertError("Ocurrió un error inesperado. Intentá más tarde.")
    }finally {
        overlay.style.display = "none" // oculta el overlay (pantalla de carga)
    }
}