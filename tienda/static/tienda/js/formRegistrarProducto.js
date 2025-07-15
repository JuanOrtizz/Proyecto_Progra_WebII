import {validarFormulario} from './validacionesFormProductos.js'
import {generarAlertExito, generarAlertError} from './alertas.js'
import {textoErrorInput, eliminarErrorInput} from './erroresInputs.js'

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
    const overlay = document.getElementById("pantalla_carga") // Obtiene el overlay (pantalla de carga)
    overlay.style.display = "flex" // Muestra el overlay (pantalla de carga)
    // hago fetch del formulario
    try
    {
        const response = await fetch("/dashboard/productos/registrar-producto/",{
            method:"POST",
            body: formData,
            headers:{
                "X-CSRFToken": csrfToken
            }
        })

        const data = await response.json()
        if(data.success){
            // vacio el formulario
            formularioProducto.reset()
            // elimino la clase de forma manual del select para que no parezca que sigue seleccionado al vaciar el formulario
            document.querySelectorAll('.select_seleccionado, .select_no_seleccionado').forEach(el => el.classList.remove('select_seleccionado', 'select_no_seleccionado'))
            // guarda en el sessionStorage el mensaje de exito para mostrar en productos.html
            sessionStorage.setItem('mensajeExito', data.message)
            window.location.href = "/dashboard/productos/" //redirige a productos.html
        }else{
            const errores = data.errors //capturo los errores
            for (let campo in errores) {
                const mensaje = errores[campo][0]
                const input = document.getElementById(campo)
                if(input) {
                    textoErrorInput(input, mensaje)
                }
            }
        }
    }catch(error){
        console.error("Error en el Registro: ", error)
        generarAlertError("Ocurrió un error inesperado. Intentá más tarde.")
    }
    finally {
        overlay.style.display = "none" // oculta el overlay (pantalla de carga)
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