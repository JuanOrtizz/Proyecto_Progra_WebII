// funcion para generar alerta de exito
export function generarAlertExito(texto){
    Swal.fire({
          title: `${texto}`,
          icon: "success",
          iconColor: '#90ee90',
          confirmButtonText: "Cerrar",
          confirmButtonColor: '#000000',
          willOpen: () => {
            const title = document.querySelector('.swal2-title')
            title.style.fontSize = '1rem'
            title.style.fontFamily = '"Nunito Sans", sans-serif'
          },
          didOpen: () =>{ // agrego esto ya que sino recalcula con esta clase y sube el footer para evitar scroll
            document.body.classList.remove('swal2-height-auto');
            document.body.style.overflow = 'auto';
            document.body.style.paddingRight = '0';
          }
    })
}

// funcion para generar alerta de error
export function generarAlertError(texto){
    Swal.fire({
        title: `${texto}`,
        icon: "error",
        iconColor: '#FF0000',
        confirmButtonText: "Cerrar",
        confirmButtonColor: '#000000',
        willOpen: () => {
            const title = document.querySelector('.swal2-title')
            title.style.fontSize = '1rem'
            title.style.fontFamily = '"Nunito Sans", sans-serif'
        },
        didOpen: () =>{ // agrego esto ya que sino recalcula con esta clase y sube el footer para evitar scroll
            document.body.classList.remove('swal2-height-auto');
            document.body.style.overflow = 'auto';
            document.body.style.paddingRight = '0';
        }
    })
}