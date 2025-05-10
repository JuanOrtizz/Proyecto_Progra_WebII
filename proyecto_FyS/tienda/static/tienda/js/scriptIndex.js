/*Uso unicamente esta funcion lambda de JS ya que al cambiar de boton del modal por el del formulario,
necesito implementarla para que funcione*/
document.addEventListener("DOMContentLoaded", function () {
  var modalElement = document.getElementById('exampleModal')
  if (modalElement) {
    var myModal = new bootstrap.Modal(modalElement)
    myModal.show()
  }
})
