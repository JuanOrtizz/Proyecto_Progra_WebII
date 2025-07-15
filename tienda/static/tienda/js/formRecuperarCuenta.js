import {validarFormulario} from './validacionesFormsContrasenia.js'
import {generarAlertExito, generarAlertError} from './alertas.js'
import {textoErrorInput, eliminarErrorInput} from './erroresInputs.js'

document.addEventListener('DOMContentLoaded', ()=>{
    // capturo el formulario y el token
    const formularioRecuperarCuenta = document.getElementById("form_recuperacion")
    const csrfToken = document.querySelector('[name = csrfmiddlewaretoken]').value

    // Evento para evitar que se mande el form
    formularioRecuperarCuenta.addEventListener('submit', (e) =>{
        // evita recargar la pagina al mandar el formulario
        e.preventDefault()
        // captura los datos del formulario
        const formData = new FormData(formularioRecuperarCuenta)
        // valida los campos
        if(validarFormulario(formData)){
            enviarFormulario(formData, csrfToken, formularioRecuperarCuenta)
        }
    })
})

// funcion async para utilizar await y manejar asincronia
async function enviarFormulario(formData, csrfToken, formularioRecuperarCuenta){
    const overlay = document.getElementById("pantalla_carga") // Obtiene el overlay (pantalla de carga)
    overlay.style.display = "flex" // Muestra el overlay (pantalla de carga)
    const botonFormulario = document.getElementById("boton_recuperar_cuenta")
    const textoOriginalBoton = botonFormulario.textContent
    let tiempoBoton = 60
    // hago fetch del formulario
    try
    {
        const response = await fetch("/recuperar-cuenta/",{
            method:"POST",
            body: formData,
            headers:{
                "X-CSRFToken": csrfToken
            }
        })
        const data = await response.json()
        if(data.success){
            generarAlertExito(data.message)
            formularioRecuperarCuenta.reset()
            //Deshabilito el boton y le agrego la clase
            botonFormulario.disabled = true
            botonFormulario.classList.add("deshabilitado")
            // Le cambio el texto
            botonFormulario.textContent = `Reintentar en ${tiempoBoton}s`

            //Intervalo para actualizar el texto del boton con un contador
            const intervalo = setInterval(() => {
                tiempoBoton--// voy restando el tiempo inicial (1 minuto)
                botonFormulario.textContent = `Reintentar en ${tiempoBoton}s` // Actualizo el texto dle boton
                //Si el tiempo es menor o igual a 0 finalizo el intervalo, activo el boton y le devuelvo el texto original
                if (tiempoBoton <= 0) {
                    clearInterval(intervalo)
                    botonFormulario.disabled = false
                    botonFormulario.textContent = textoOriginalBoton
                    botonFormulario.classList.remove("deshabilitado")
                }
            }, 1000) // Intervalo de 1 segundo
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
        console.error("Error en la Recuperación: ", error)
        generarAlertError("Ocurrió un error inesperado. Intentá más tarde.")
    }finally {
        overlay.style.display = "none" // oculta el overlay (pantalla de carga)
    }
}