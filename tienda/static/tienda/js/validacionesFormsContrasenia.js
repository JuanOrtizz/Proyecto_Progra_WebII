// funcion para validar el formulario
export function validarFormulario(formData){
    let esValido = true // al comienzo siempre va a ser valido
    let contraseña = ""

    // recorre cada input del formulario y realiza las validaciones con sus metodos
    for(let [llave, valor] of formData.entries()){
        const input = document.getElementById(llave)

        if (!input) {
            continue
        }

        input.addEventListener('focus', ()=>{
            input.classList.remove("input_error")
            eliminarErrorInput(input)
        })

        valor = valor.trim()
        if(!valor){
            textoErrorInput(input, "El campo está vacío")
            esValido = false
        }
        else if (llave === "email"){
            if(!validarInputEmail(input, valor)) esValido = false
        }
        else if (llave === "contraseña"){
            contraseña = valor
            if(!validarInputContraseña(input, valor))esValido = false
        }else if (llave === 'confirmar_contraseña'){
            if(!validarInputConfirmarContraseña(input, valor, contraseña))esValido = false
        }
    }
    return esValido
}

// funcion para aplicar error (span)
function textoErrorInput(input, mensaje) {
    const errorSpan = document.getElementById(`error-${input.id}`)
    if (errorSpan) {
        errorSpan.textContent = mensaje
        errorSpan.style.display = 'block'
        input.classList.add("input_error")
    }
}

// funcion para eliminar error (span)
function eliminarErrorInput(input) {
    const errorSpan = document.getElementById(`error-${input.id}`)
    if (errorSpan) {
        errorSpan.textContent = ''
        errorSpan.style.display = 'none'
        input.classList.remove("input_error")
    }
}

//validar input email
function validarInputEmail(input, valor){
    const patron = /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/ // verifica si es un email valido
    if(valor.length >= 6 && valor.length <= 100){
        if (!patron.test(valor)){
            textoErrorInput(input, "El email no es válido")
            return false
        }
    }else{
        textoErrorInput(input, "Email: de 6 a 100 caracteres")
        return false
    }
    return true
}

//validar input contraseña
function validarInputContraseña(input, valor) {
    const patron = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$/
    if (valor.length >= 8 && valor.length <= 20) {
        if (!patron.test(valor)) {
            textoErrorInput(input, "La contraseña debe contener mayúsculas, minúsculas y números")
            return false
        }
    } else {
        textoErrorInput(input, "Contraseña: 8 a 20 caracteres")
        return false
    }
    return true
}

//validar input contraseña
function validarInputConfirmarContraseña(input, valor, contraseña) {
    if (valor !== contraseña) {
        textoErrorInput(input, "Las contraseñas no coinciden")
        return false
    }
    return true
}