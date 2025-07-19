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

        if (llave === "imagen"){
            if(!validarInputImagen(input))esValido = false
        }else{
            valor = valor.trim()
            if(!valor){
                textoErrorInput(input, "El campo está vacío")
                esValido = false
            }
            else if (llave === "nombre"){
                if(!validarInputNombre(input, valor)) esValido = false
            }
            else if (llave === "precio"){
                if(!validarInputPrecio(input, valor)) esValido = false
            }
            else if (llave === "tipo"){
                if(!validarSelectTipoProducto(input, valor)) esValido = false
            }
        }
    }
    return esValido
}

// Validaciones propias para cada campo
// validar input nombre
function validarInputNombre(input, valor){
    const patron = /^[a-záéíóúñ0-9]+(?:\s[a-záéíóúñ0-9]+)*$/i // verifica si es un nombre con solo letras Upper y Lower, numeros y espacios
    if(valor.length >= 2 && valor.length <= 100){
        if (!patron.test(valor)){
            textoErrorInput(input, "El nombre no es válido")
            console.log("error")
            return false
        }
    }else{
        textoErrorInput(input, "Nombre: de 2 a 100 caracteres")
        return false
    }
    return true
}

// validar input precio producto
function validarInputPrecio(input, valor){
    const regexPrecio = /^\d{1,7}(\.\d{1,2})?$/;
    if (regexPrecio.test(valor)){
        const valorNumerico = parseFloat(valor)
        if(valorNumerico < 1){
            textoErrorInput(input, "Precio mínimo: $1")
            return false
        }else if (valorNumerico > 9999999.99){
            textoErrorInput(input, "Precio máximo: $9.999.999,99")
            return false
        }
    }else{
        textoErrorInput(input, "El precio no es válido (Máximo 2 decimales)")
        return false
    }
    return true
}

//validar select tipo de producto
function validarSelectTipoProducto(select, valor){
    if (valor && valor !== ""){
        select.classList.remove("input_error")
        return true
    }else{
        select.classList.add("input_error")
        return false
    }
}

// validar input archivo (solo 1 archivo, JPG o PNG, máx 5 MB)
function validarInputImagen(input) {
    // Si se permite solo un archivo, input.files tendrá máximo 1 elemento
    const imagen = input.files[0]
    const tiposImagen = ['image/webp']
    const maxTamanoMB = 1
    if (!imagen) {
        textoErrorInput(input, "El producto debe tener una imagen")
        return false
    }
    else if (!tiposImagen.includes(imagen.type)){
        textoErrorInput(input, "La imagen debe ser en formato WEBP")
        return false
    }
    else if (imagen.size > maxTamanoMB * 1024 * 1024) {
        textoErrorInput(input, `La imagen no puede superar los ${maxTamanoMB} MB`)
        return false
    }
    return true
}
