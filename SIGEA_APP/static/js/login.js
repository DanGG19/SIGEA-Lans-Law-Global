const contraseña = document.getElementById('password');
const iconoOjo =   document.querySelector('i');

const mostrarContraseña = () => {
    if(contraseña.type == 'password'){
        contraseña.type = 'text';
        iconoOjo.classList.remove('fa-eye');
        iconoOjo.classList.add('fa-eye-slash');
    }else{
        contraseña.type = 'password';
        iconoOjo.classList.remove('fa-eye-slash');
        iconoOjo.classList.add('fa-eye');
    }
}
iconoOjo.addEventListener('click', mostrarContraseña);