document.addEventListener("DOMContentLoaded", () => {
  var modalElement = document.getElementById('exampleModal')
  var botonEnviarFormulario = document.getElementById('boton_enviar_form')

  if (modalElement) {
    var myModal = new bootstrap.Modal(modalElement)

    // muestro el modal
    myModal.show()

    //cuando el modal se cierra, mueve el foco al boton que lo abrio (boton del formulario)
    modalElement.addEventListener('hidden.bs.modal', () => {
      botonEnviarFormulario.focus()

      // borra estilos aplicados por el modal (como el fondo oscuro)
      myModal.dispose()

      // vuelvo el estilo overflow para permitir el scroll
      document.body.style.overflow = ''

      // elimino el margen que le pone el modal al body
      document.body.style.paddingRight = '0px'
    })
  }
})