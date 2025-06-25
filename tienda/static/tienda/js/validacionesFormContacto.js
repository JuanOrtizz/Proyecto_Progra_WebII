// funcion para validar el formulario
export function validarFormulario(formData){
    let esValido = true // al comienzo siempre va a ser valido

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
            textoErrorInput(input, "El campo esta vacío")
            esValido = false
        }
        else if (llave === "nombre"){
            if(!validarInputNombre(input, valor)) esValido = false
        }
        else if (llave === "email"){
            if(!validarInputEmail(input, valor)) esValido = false
        }
        else if (llave === "telefono"){
            if(!validarInputCelular(input, valor)) esValido = false
        }
        else if (llave === "mensaje"){
           if(!validarTextarea(input, valor))esValido = false
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

// Validaciones propias para cada campo
// validar input nombre
function validarInputNombre(input, valor){
    const patron = /^[a-záéíóúñ]+(?:\s[a-záéíóúñ]+)*$/i // verifica si es un nombre con solo letras Upper y Lower y espacios
    if(valor.length >= 2 && valor.length <= 100){
        if (!patron.test(valor)){
            textoErrorInput(input, "El nombre es invalido")
            console.log("error")
            return false
        }
    }else{
        textoErrorInput(input, "Nombre: 2 a 100 caracteres")
        return false
    }
    return true
}

//validar input email
function validarInputEmail(input, valor){
    const patron = /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/ // verifica si es un email valido
    if(valor.length >= 6 && valor.length <= 100){
        if (!patron.test(valor)){
            textoErrorInput(input, "El email es invalido")
            return false
        }
    }else{
        textoErrorInput(input, "Email: 6 a 100 caracteres")
        return false
    }
    return true
}

//validar input celular
function validarInputCelular(input, valor){
    const patron =  /^\+?[0-9]{6,25}$/ // verifica si es un celular valido
    if(valor.length >= 6 && valor.length <= 25){
        if (!patron.test(valor)){
            textoErrorInput(input, "El celular es invalido")
            return false
        }
    }else{
        textoErrorInput(input, "Celular: 6 a 25 caracteres")
        return false
    }
    return true
}

// validar textarea
function validarTextarea(input, valor){
    if(valor.length < 2 || valor.length > 1000){
        textoErrorInput(input, "Mensaje: 2 a 1000 caracteres")
        return false
    }
    return true
}