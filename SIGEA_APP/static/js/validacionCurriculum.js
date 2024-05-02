
(function () {
    'use strict';
    var formulario = document.querySelectorAll('.needs-validation');
    Array.prototype.slice.call(formulario).forEach(function (form) {
        form.addEventListener('submit', function (event) {
            
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
                var elementosInvalidos = form.querySelectorAll(':invalid');
                elementosInvalidos[0].focus();
            }
            form.classList.add('was-validated');
        }, false);
    })
})();  // Los paréntesis aquí invocan la función anónima inmediatamente