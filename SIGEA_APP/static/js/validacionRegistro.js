// validar contraseña igual 
function checkPasswordMatch() {
    var password = document.getElementById('clave');
    var confirm_password = document.getElementById('clave2');
    if (password.value != confirm_password.value) {
        confirm_password.setCustomValidity('Las contraseñas no coinciden');
    } else {
        confirm_password.setCustomValidity('');
    }
}

//Validaciones del formulario de registro
(function () {
    'use strict';
    //obtener el formulario de registro
    var formulario = document.querySelectorAll('.needs-validation');
    Array.prototype.slice.call(formulario).forEach(function (form) {
        form.addEventListener('submit', function (event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
                
                // Obtener todos los elementos inválidos del formulario
                var elementosInvalidos = form.querySelectorAll(':invalid');
                
                // Enfocar el primer elemento inválido
                elementosInvalidos[0].focus();
            }
            form.classList.add('was-validated');
        }, false);
    })
})()
