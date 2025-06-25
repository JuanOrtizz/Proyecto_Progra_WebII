import {generarAlertError} from './alertas.js' // importo la alerta
import {validarFormulario} from './validacionesFormContacto.js' // Importo las validaciones

document.addEventListener('DOMContentLoaded', ()=>{

    // capturo el formulario y el token
    const formularioModificarConsulta = document.getElementById("form_modificar_consulta")
    const csrfToken = document.querySelector('[name = csrfmiddlewaretoken]').value

    // Evento para evitar que se mande el form
    if(formularioModificarConsulta){
            formularioModificarConsulta.addEventListener('submit', (e) =>{
                // evita recargar la pagina al mandar el formulario
                e.preventDefault()
                // captura los datos del formulario
                let formData = new FormData(formularioModificarConsulta)
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
        if(data.success){
            // guarda en el sessionStorage el mensaje de exito para mostrar en dashboard.html
            sessionStorage.setItem('mensajeExito', data.message)
            window.location.href = "/dashboard/consultas/" //redirige a dashboard.html
        }else{
            if(data.errors){
                generarAlertError(data.errors)
            }
            else{
                generarAlertError("Ocurrió un error al modificar la consulta. Intenta nuevamente")
            }
        }
    }catch(error){
        console.error("Error en la modificación: ", error)
        generarAlertError("Error al modificar la consulta. Intenta mas tarde")
    }
}