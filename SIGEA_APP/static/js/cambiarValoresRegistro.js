// Obtener el elemento select y el campo de entrada oculto
var sexo = document.getElementById('sexo');
var sexoTexto = document.getElementById('sexo_texto');

// Agregar un controlador de eventos change
sexo.addEventListener('change', function() {
    // Obtener el índice del elemento seleccionado
    var selectedIndex = this.selectedIndex;

    // Obtener el texto del elemento seleccionado
    var selectedText = this.options[selectedIndex].text;

    // Actualizar el valor del campo de entrada oculto
    sexoTexto.value = selectedText;
    
});
// Obtener el elemento select y el campo de entrada oculto
var genero = document.getElementById('genero');
var generoTexto = document.getElementById('genero_texto');
// Agregar un controlador de eventos change
genero.addEventListener('change', function() {
    // Obtener el índice del elemento seleccionado
    var selectedIndex = this.selectedIndex;

    // Obtener el texto del elemento seleccionado
    var selectedText = this.options[selectedIndex].text;

    // Actualizar el valor del campo de entrada oculto
    generoTexto.value = selectedText;
}); 
// Obtener el elemento select y el campo de entrada oculto
var pais = document.getElementById('pais');
var paisTexto = document.getElementById('pais_texto');
// Agregar un controlador de eventos change
pais.addEventListener('change', function() {
    // Obtener el índice del elemento seleccionado
    var selectedIndex = this.selectedIndex;

    // Obtener el texto del elemento seleccionado
    var selectedText = this.options[selectedIndex].text;

    // Actualizar el valor del campo de entrada oculto
    paisTexto.value = selectedText;
});
// Obtener el elemento select y el campo de entrada oculto
var carrera = document.getElementById('carrera');
var carreraTexto = document.getElementById('carrera_texto');
// Agregar un controlador de eventos change
carrera.addEventListener('change', function() {
    // Obtener el índice del elemento seleccionado
    var selectedIndex = this.selectedIndex;

    // Obtener el texto del elemento seleccionado
    var selectedText = this.options[selectedIndex].text;

    // Actualizar el valor del campo de entrada oculto
    carreraTexto.value = selectedText;
});