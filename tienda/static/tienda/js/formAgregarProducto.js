import {validarFormulario} from './validacionesFormProductos.js'
import {generarAlertExito, generarAlertError} from './alertas.js'

document.addEventListener('DOMContentLoaded', ()=>{
    // capturo el select para aplicarle un estilo para mejorar UX
    const selectTipoProducto = document.getElementById("tipo")
    selectTipoProducto.addEventListener('change',()=>{
        asignarClaseSelect(selectTipoProducto, selectTipoProducto.value.trim())
    })

    // capturo el formulario y el token
    const formularioProducto = document.getElementById("form_producto")
    const csrfToken = document.querySelector('[name = csrfmiddlewaretoken]').value

    // Evento para evitar que se mande el form
    formularioProducto.addEventListener('submit', (e) =>{
            // evita recargar la pagina al mandar el formulario
            e.preventDefault()
            // captura los datos del formulario
            const formData = new FormData(formularioProducto)
            // valida los campos
            if(validarFormulario(formData)){
                enviarFormulario(formData, csrfToken, formularioProducto)
            }
        })
})

// funcion async para utilizar await y manejar asincronia
async function enviarFormulario(formData, csrfToken, formularioProducto){
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
            formularioProducto.reset()

            // elimino la clase de forma manual del select para que no parezca que sigue seleccionado al vaciar el formulario
            document.querySelectorAll('.select_seleccionado, .select_no_seleccionado').forEach(el => el.classList.remove('select_seleccionado', 'select_no_seleccionado'))

        }else{
            generarAlertError(formatearErrores(data.errors))
        }
    }catch(error){
        console.error("Error en el Registro: ", error)
        generarAlertError("Ocurrió un error inesperado. Intentá más tarde.")
    }
}

// funcion para asignar una clase al select para que cambie si se eligio un valor o no en el formulario, para mejorar la UX
function asignarClaseSelect(select, valor){
    if(valor && valor !== ""){
        select.classList.add("select_seleccionado")
        select.classList.remove("select_no_seleccionado")
    }else{
        select.classList.add("select_no_seleccionado")
        select.classList.remove("select_seleccionado")
    }
}

function formatearErrores(errores) {
    let mensajes = []
    for (const campo in errores) {
        if (errores.hasOwnProperty(campo)) {
          mensajes.push(`${campo}: ${errores[campo].join(', ')}`)
        }
    }
    return mensajes.join('\n')
}