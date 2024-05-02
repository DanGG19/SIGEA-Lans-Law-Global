document.addEventListener('DOMContentLoaded', function () {
    document.addEventListener('click', function (event) {
        if (event.target.matches('[id^="aplicar"]')) {
            //Para obtener el boton que se toca
            var boton = event.target;
            //Para obtener la tarjeta que se toca
            var cardId = boton.id.replace('aplicar', 'card');
            var card = document.getElementById(cardId);
            //Para obtener los datos de la tarjeta
            //Obtener sueldo
            var sueldoId = 'sueldo' + cardId.replace('card', '');
            var sueldoElement = document.getElementById(sueldoId);
            var sueldo = sueldoElement.textContent;
            //Obtener cargo
            var cargoId = 'cargo' + cardId.replace('card', '');
            var cargoElement = document.getElementById(cargoId);
            var cargo = cargoElement.textContent;
            //Obtener nombre de la empresa
            var nombreEmpresaID = 'empresa' + cardId.replace('card', '');
            var empresaElement = document.getElementById(nombreEmpresaID);
            var nombreEmpresa = empresaElement.textContent;
            //Obtener direccion de la empresa
            var direccionID = 'direccion' + cardId.replace('card', '');
            var direccionElement = document.getElementById(direccionID);
            var direccion = direccionElement.textContent;
            //Obtener el id de la empresa
            var idEmpresaID = 'idEmpresa' + cardId.replace('card', '');
            var idEmpresaElement = document.getElementById(idEmpresaID);
            var idEmpresa = idEmpresaElement.value;
            console.log(idEmpresa);
            //Obtener el id del usuario
            var userId = document.getElementById('userId').value;
            //Obtener el id del currículum
            var currículumId = document.getElementById('curriculumId').value;
            //Obtener los datos del currículum
            var curriculumData;
            //Obtener el token de seguridad
            function getCookie(name) {
                var cookieValue = null;
                if (document.cookie && document.cookie !== '') {
                    var cookies = document.cookie.split(';');
                    for (var i = 0; i < cookies.length; i++) {
                        var cookie = cookies[i].trim();
                        if (cookie.substring(0, name.length + 1) === (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }
            //Solicitud fetch para obtener los datos del currículum
            fetch('http://127.0.0.1:8000/apicurriculum/'+currículumId+'')
                .then(response => response.json())
                .then(data => {
                    console.log(data);  // Aquí puedes acceder a `los datos del currículum
                    curriculumData = data;
                }).then(() => {

            var csrftoken = getCookie('csrftoken');
            //Solicitud fetch para guardar la solicitud
            fetch('http://127.0.0.1:8000/apisolicitud/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({
                    
                    nombre_empresa: nombreEmpresa,
                    cargo_aspirado: cargo,
                    direccion_empresa: direccion,
                    sueldo: sueldo,
                    user: userId,
                    
                }),
            }).then(Response => {
                if (Response.ok) {
                    return Response.json();
                } else {
                    throw new Error('Error al guardar la solicitud');
                }
            }).then(data => {
                console.log("Solicitud guardada con exito.");
                swal.fire({
                    title: 'Curriculum enviado con exito a la empresa: ' + data.nombre_empresa,
                    icon: 'success',
                    confirmButtonText: 'Aceptar',
                })
                
            })
            .catch((error) => console.error('Error:', error));
        });
        }
    });
});