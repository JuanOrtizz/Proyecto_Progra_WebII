document.addEventListener('DOMContentLoaded', ()=>{
    // capturo el select para realizar submit y procesarlo en el backend
    const selectTipoProducto = document.getElementById("filtro_tipo")
    selectTipoProducto.addEventListener('change',()=>{
        selectTipoProducto.form.submit()
    })
})