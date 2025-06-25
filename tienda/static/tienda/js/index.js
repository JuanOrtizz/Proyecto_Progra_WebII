document.addEventListener('DOMContentLoaded', () => {
    // creo una nueva instancia de IntersectionObserver que va a observar elementos que entren o salgan del viewport
    const observer = new IntersectionObserver(entries => {

        // recorre todas las entradas (elementos observados)
        entries.forEach(entry => {
            // si el elemento esta visible (intersectando con el viewport)
            if (entry.isIntersecting) {
                // le agrega la clase 'aparecer' al elemento que entro en vista
                entry.target.classList.add('aparecer')
            }
        })
    }, {
        //se activa cuando el 20% del elemento sea visible
        threshold: 0.2
    })

    // selecciona todos los elementos con esas clases y empieza a observarlos con el observer
    document.querySelectorAll('.contenedor_izquierda, .contenedor_derecha').forEach(el => {
        observer.observe(el)
    })
})