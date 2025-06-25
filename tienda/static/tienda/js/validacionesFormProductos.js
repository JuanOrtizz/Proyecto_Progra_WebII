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

        if (llave === "imagen"){
            if(!validarInputImagen(input))esValido = false
        }else{
            valor = valor.trim()
            if(!valor){
                textoErrorInput(input, "El campo esta vacío")
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

// validar input precio producto
function validarInputPrecio(input, valor){
    const valorNumerico = parseFloat(valor, 10.2)
    if (!isNaN(valorNumerico)){
        if(valorNumerico < 1){
            textoErrorInput(input, "Precio minimo: $1")
            return false
        }else if (valorNumerico > 9999999.99){
            textoErrorInput(input, "Precio Máximo: $9,999,999.99")
            return false
        }
    }else{
        textoErrorInput(input, "Precio invalido")
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
        textoErrorInput(input, "La imagen no puede superar los " + maxTamanoMB + " MB")
        return false
    }
    return true
}
