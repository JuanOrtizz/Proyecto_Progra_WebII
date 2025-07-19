import {textoErrorInput, eliminarErrorInput} from './erroresInputs.js'
// funcion para validar el formulario
export function validarFormulario(formData){
    let esValido = true // al comienzo siempre va a ser valido

    // recorre cada input del formulario y realiza las validaciones con sus metodos
    for(let [llave, valor] of formData.entries()){
        const input = document.getElementById(`id_${llave}`)
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

// Validaciones propias para cada campo
// validar input nombre
function validarInputNombre(input, valor){
    const patron = /^[a-záéíóúñ]+(?:\s[a-záéíóúñ]+)*$/i // verifica si es un nombre con solo letras Upper y Lower y espacios
    if(valor.length >= 2 && valor.length <= 100){
        if (!patron.test(valor)){
            textoErrorInput(input, "El nombre no es válido")
            return false
        }
    }else{
        textoErrorInput(input, "Nombre: de 2 a 100 caracteres")
        return false
    }
    return true
}

//validar input email
function validarInputEmail(input, valor){
    const patron = /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/ // verifica si es un email valido
    if(valor.length >= 6 && valor.length <= 254){
        if (!patron.test(valor)){
            textoErrorInput(input, "El email no es válido")
            return false
        }
    }else{
        textoErrorInput(input, "Email: de 6 a 254 caracteres")
        return false
    }
    return true
}

//validar input celular
function validarInputCelular(input, valor){
    const patron =  /^\+?[0-9]{6,25}$/ // verifica si es un celular valido
    if(valor.length >= 6 && valor.length <= 25){
        if (!patron.test(valor)){
            textoErrorInput(input, "El celular no es válido")
            return false
        }
    }else{
        textoErrorInput(input, "Celular: de 6 a 25 caracteres")
        return false
    }
    return true
}

// validar textarea
function validarTextarea(input, valor){
    if(valor.length < 2 || valor.length > 1000){
        textoErrorInput(input, "Mensaje: de 2 a 1000 caracteres")
        return false
    }
    return true
}