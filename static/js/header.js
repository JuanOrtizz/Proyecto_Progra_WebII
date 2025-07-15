// Agrego un event listener al cargar el dom
document.addEventListener("DOMContentLoaded",  () => {
    // capturo el menu hamburguesa y la lista (UL) de enlaces
    const menuHamburguesa = document.getElementById("menu_hamburguesa")
    const listaEnlaces = document.getElementById("lista_enlaces")

    // Capturo el elemento (LI) si el usuario esta logeado y todos sus elementos hijos
    const elementoDropdown = document.getElementById("usuario_dropdown")
    const contenedorUsuarioLogeado = document.getElementById("contenedor_usuario")
    const menuUsuarioDropdown = document.getElementById("menu_usuario")
    const flechaDropdown = document.getElementById("flecha_usuario")

    // capturo la direccion actual y todos los enlaces de la lista (UL) y sus elementos (LI)
    const pathActual = window.location.pathname
    const enlaces = document.querySelectorAll('li a')

    // EventListener para el menu hamburguesa
    menuHamburguesa.addEventListener("click",  (e) => {
        e.stopPropagation() // evito que se propague al document
        listaEnlaces.classList.toggle("activo") // le pongo o saco la clase activo a los enlaces
        menuHamburguesa.classList.toggle("rotacion") // le pongo o saco la clase rotacion a el menu hamburguesa para una animacion
    })

    // EventListener para el submenu del elemento Usuario Logeado
    if(contenedorUsuarioLogeado){
        contenedorUsuarioLogeado.addEventListener("click", (e) => {
            if (esPantallaChica()) { // si la pantalla chica lo expande
                e.stopPropagation() // evito que se propague al document
                menuUsuarioDropdown.classList.toggle("abierto") // Le pongo la clase abierto al submenu
                flechaDropdown.classList.toggle("abierta") // le pongo la clase abierta al icon dropdown del submenu
            }
        })
    }

    //foreach para recorrer cada link del array
    enlaces.forEach(a => {
        //si el enlace del <a> es igual a la direccion actual de la pagina le agrego la clase para que aparezca como marcado para mejorar UX
        if(a.pathname === pathActual){
            a.classList.add('enlace_activo')
        }
      })

    // Cierra el menu si se hace clic en el documento y si no esta dentro de ninguno de los elementos puestos en el if
    document.addEventListener("click", (e) => {
        if (esPantallaChica()) { // Si la pantalla es chica
            // Si el click no esta dentro de ninguno de estos elementos cierra el menu hamburguesa y el submenu
            if (!elementoDropdown?.contains(e.target) && !menuHamburguesa?.contains(e.target) && !listaEnlaces?.contains(e.target)) {
                menuUsuarioDropdown?.classList.remove("abierto")
                flechaDropdown?.classList.remove("abierta")
                listaEnlaces?.classList.remove("activo")
                menuHamburguesa?.classList.remove("rotacion")
            }
        }
    })
})

// funcion para calcular si la pantalla es chica
function esPantallaChica() {
    return window.innerWidth <= 768
}