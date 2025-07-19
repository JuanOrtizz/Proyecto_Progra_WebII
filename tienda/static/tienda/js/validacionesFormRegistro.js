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
            if(!validarInputNombreCompleto(input, valor)) esValido = false
        }
        else if (llave === "apellido"){
            if(!validarInputNombreCompleto(input, valor)) esValido = false
        }
        else if (llave === "email"){
            if(!validarInputEmail(input, valor)) esValido = false
        }
        else if (llave === "contrasenia"){
            if(!validarInputContrasenia(input, valor))esValido = false
        }else if (llave === 'codigo'){
            if(!validarInputCodigo(input, valor))esValido = false
        }
    }
    return esValido
}

// Validaciones propias para cada campo
// validar input nombre y apellido
function validarInputNombreCompleto(input, valor){
    const patron = /^[a-záéíóúñ]+(?:\s[a-záéíóúñ]+)*$/i // verifica si es un nombre con solo letras Upper y Lower y espacios
    if(valor.length >= 2 && valor.length <= 100){
        if (!patron.test(valor)){
            textoErrorInput(input, `El ${input.name} no es válido`)
            console.log("error")
            return false
        }
    }else{
        textoErrorInput(input, `Campo ${input.name}: de 2 a 100 caracteres`)
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

//validar input contraseña
function validarInputContrasenia(input, valor) {
    const patron = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$/
    if (valor.length >= 8 && valor.length <= 20) {
        if (!patron.test(valor)) {
            textoErrorInput(input, "La contraseña debe contener mayúsculas, minúsculas y números")
            return false
        }
    } else {
        textoErrorInput(input, "Contraseña: de 8 a 20 caracteres")
        return false
    }
    return true
}

//Validar input codigo (Validar cuenta)
function validarInputCodigo(input,valor){
     if (valor.length != 6) {
        textoErrorInput(input, "El código debe tener 6 dígitos")
        return false
    }
    return true
}