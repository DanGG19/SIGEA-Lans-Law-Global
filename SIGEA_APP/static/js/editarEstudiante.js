//Para dropdown de pais
document.addEventListener('DOMContentLoaded', (event) => {
    const pais = document.getElementById('pais');
    const valorPais = pais.getAttribute('value');

    const opcionesPais = pais.options;

    for (let i = 0; i < opcionesPais.length; i++) {
        if (opcionesPais[i].text === valorPais) {
            opcionesPais[i].selected = true;
        }
    }
});
//Para dropdown de genero
document.addEventListener('DOMContentLoaded', (event) => {
    const genero = document.getElementById('genero');
    const valorGenero = genero.getAttribute('value');
    const opcionesGenero = genero.options;
    for (let i = 0; i < opcionesGenero.length; i++) {
        if (opcionesGenero[i].text === valorGenero) {
            opcionesGenero[i].selected = true;
        }
    }
});
//Para dropdown de sexo
document.addEventListener('DOMContentLoaded', (event) => {
    const sexo = document.getElementById('sexo');
    const valorSexo = sexo.getAttribute('value');
    const opcionesSexo = sexo.options;
    for (let i = 0; i < opcionesSexo.length; i++) {
        if (opcionesSexo[i].text === valorSexo) {
            opcionesSexo[i].selected = true;
        }
    }
});
//Para dropdown de carrera
document.addEventListener('DOMContentLoaded', (event) => {
    const carrera = document.getElementById('carrera');
    const valorCarrera = carrera.getAttribute('value');
    const opcionesCarrera = carrera.options;
    for (let i = 0; i < opcionesCarrera.length; i++) {
        if (opcionesCarrera[i].text === valorCarrera) {
            opcionesCarrera[i].selected = true;
        }
    }
});

window.onload = function() {
    // Obtener el elemento select y el campo de entrada oculto
    var sexo = document.getElementById('sexo');
    var sexoTexto = document.getElementById('sexo_texto');
    var genero = document.getElementById('genero');
    var generoTexto = document.getElementById('genero_texto');
    var pais = document.getElementById('pais');
    var paisTexto = document.getElementById('pais_texto');
    var carrera = document.getElementById('carrera');
    var carreraTexto = document.getElementById('carrera_texto');

    // Función para actualizar el valor del campo de entrada oculto
    function updateHiddenInput(selectElement, hiddenInputElement) {
        var selectedIndex = selectElement.selectedIndex;
        var selectedText = selectElement.options[selectedIndex].text;
        hiddenInputElement.value = selectedText;
    }

    // Actualizar los valores iniciales
    updateHiddenInput(sexo, sexoTexto);
    updateHiddenInput(genero, generoTexto);
    updateHiddenInput(pais, paisTexto);
    updateHiddenInput(carrera, carreraTexto);

    // Agregar controladores de eventos change
    sexo.addEventListener('change', function() {
        updateHiddenInput(sexo, sexoTexto);
    });
    genero.addEventListener('change', function() {
        updateHiddenInput(genero, generoTexto);
    });
    pais.addEventListener('change', function() {
        updateHiddenInput(pais, paisTexto);
        console.log(paisTexto.value);
    });
    carrera.addEventListener('change', function() {
        updateHiddenInput(carrera, carreraTexto);
    });
}