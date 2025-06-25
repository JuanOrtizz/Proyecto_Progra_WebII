// Agrego un event listener al cargar el dom
document.addEventListener("DOMContentLoaded",  () => {
    // capturo el menu hamburguesa y la lista (UL) de enlaces
    const menuHamburguesa = document.getElementById("menu_hamburguesa")
    const listaEnlaces = document.getElementById("lista_enlaces")
    // capturo la direccion actual y todos los enlaces de la lista (UL) y sus elementos (LI)
    const pathActual = window.location.pathname
    const enlaces = document.querySelectorAll('li a')

    // EventListener para el menu hamburguesa
    menuHamburguesa.addEventListener("click",  () => {
        listaEnlaces.classList.toggle("activo") // le pongo o saco la clase activo a los enlaces
        menuHamburguesa.classList.toggle("rotacion") // le pongo o saco la clase rotacion a el menu hamburguesa para una animacion
    })

    //foreach para recorrer cada link del array
    enlaces.forEach(a => {
        //si el enlace del <a> es igual a la direccion actual de la pagina le agrego la clase para que aparezca como marcado para mejorar UX
        if(a.pathname === pathActual){
            a.classList.add('enlace_activo')
        }
      })

})