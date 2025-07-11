document.addEventListener('DOMContentLoaded', () => {
     const parrafoFrase = document.getElementById('frase_motivadora')
     obtenerFrase(parrafoFrase)
})

// Funcion asincrona para obtener la frase desde el backend
async function obtenerFrase(parrafoFrase) {
    try {
        const response = await fetch('/obtener_frase/')
        const data = await response.json();
        if(parrafoFrase){
            parrafoFrase.textContent = data.frase
        }
    } catch (error) {
        console.error('Error al obtener la frase:', error)
    }
}
