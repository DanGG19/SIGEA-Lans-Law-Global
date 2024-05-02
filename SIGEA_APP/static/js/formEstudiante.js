var vistaPrevia_doc = document.getElementById('vista-previa_doc');
        vistaPrevia_doc.style.display = 'block';

        // Ajusta el tamaño de la imagen
        vistaPrevia_doc.style.width = '150px';  // Ajusta el ancho a 200px
        vistaPrevia_doc.style.height = 'auto';  // Ajusta la altura automáticamente para mantener la proporción de la imagen
        //centrar imagen
        vistaPrevia_doc.style.display = 'block';
        vistaPrevia_doc.style.margin = '0 auto';
        //Vista previa tamaño de imagen de perfil
        var vistaPrevia_perfil = document.getElementById('vista-previa_perfil');
        vistaPrevia_perfil.style.display = 'block';

        // Ajusta el tamaño de la imagen
        vistaPrevia_perfil.style.width = '150px';  // Ajusta el ancho a 200px
        vistaPrevia_perfil.style.height = 'auto';  // Ajusta la altura automáticamente para mantener la proporción de la imagen
        //centrar imagen
        vistaPrevia_perfil.style.display = 'block';
        vistaPrevia_perfil.style.margin = '0 auto';
        
document.getElementById('imagen_documento').onchange = function (e) {
    // Obtén el primer archivo seleccionado
    var archivo_doc = e.target.files[0];

    // Crea un nuevo objeto FileReader
    var lector_doc = new FileReader();

    // Cuando el archivo se haya leído...
    lector_doc.onload = function (e) {
        // Usa el resultado para actualizar el src del elemento img
        var vistaPrevia_doc = document.getElementById('vista-previa_doc');
        vistaPrevia_doc.src = e.target.result;
        vistaPrevia_doc.style.display = 'block';

        // Ajusta el tamaño de la imagen
        vistaPrevia_doc.style.width = '150px';  // Ajusta el ancho a 200px
        vistaPrevia_doc.style.height = 'auto';  // Ajusta la altura automáticamente para mantener la proporción de la imagen
        //centrar imagen
        vistaPrevia_doc.style.display = 'block';
        vistaPrevia_doc.style.margin = '0 auto';
    };

    // Lee el archivo
    lector_doc.readAsDataURL(archivo_doc);
};

// para imagen de perfil
document.getElementById('imagen_perfil').onchange = function (f) {
    // Obtén el primer archivo seleccionado
    var archivo_perfil = f.target.files[0];

    // Crea un nuevo objeto FileReader
    var lector_perfil = new FileReader();

    // Cuando el archivo se haya leído...
    lector_perfil.onload = function (f) {
        // Usa el resultado para actualizar el src del elemento img
        var vistaPrevia_perfil = document.getElementById('vista-previa_perfil');
        vistaPrevia_perfil.src = f.target.result;
        vistaPrevia_perfil.style.display = 'block';

        // Ajusta el tamaño de la imagen
        vistaPrevia_perfil.style.width = '150px';  // Ajusta el ancho a 200px
        vistaPrevia_perfil.style.height = 'auto';  // Ajusta la altura automáticamente para mantener la proporción de la imagen
        //centrar imagen
        vistaPrevia_perfil.style.display = 'block';
        vistaPrevia_perfil.style.margin = '0 auto';
    };

    // Lee el archivo
    lector_perfil.readAsDataURL(archivo_perfil);
};
//Para dropdown de genero
    const genero = document.getElementById('genero');
    const valorGenero = genero.getAttribute('value');
    const generoMas= document.getElementById('generoMas');
    const generoFem= document.getElementById('generoFem');
    const generoLgb= document.getElementById('generoLgb');
    const generoOtr= document.getElementById('generoNs');

    // Crea un array con todos los elementos option
const opcionesGenero = [generoMas, generoFem, generoLgb, generoOtr];

// Recorre el array y agrega el atributo 'selected' al option que tenga el mismo valor que 'valorGenero'
opcionesGenero.forEach(function(opcion) {
    if (opcion.value === valorGenero) {
        opcion.selected = true;
    }
});
//Para dropdown de sexo hombre o mujer
 const sexo=document.getElementById('sexo');
    const valorSexo = sexo.getAttribute('value');
    const sexoMas= document.getElementById('hombre');
    const sexoFem= document.getElementById('mujer');
    // Crea un array con todos los elementos option
const opcionesSexo = [sexoMas, sexoFem];
// Recorre el array y agrega el atributo 'selected' al option que tenga el mismo valor que 'valorSexo'
opcionesSexo.forEach(function(opcion) {
    if (opcion.value === valorSexo) {
        opcion.selected = true;
    }
}); 
//Para dropdown de pais
document.addEventListener('DOMContentLoaded', (event) => {
    const pais = document.getElementById('pais');
    const valorPais = pais.getAttribute('value');

    const opcionesPais = pais.options;

    for (let i = 0; i < opcionesPais.length; i++) {
        if (opcionesPais[i].value === valorPais) {
            opcionesPais[i].selected = true;
        }
    }
});
//Para dropdown de carrera
document.addEventListener('DOMContentLoaded', (event) => {
    const carrera = document.getElementById('carrera');
    const valorCarrera = carrera.getAttribute('value');

    const opcionesCarrera = carrera.options;

    for (let i = 0; i < opcionesCarrera.length; i++) {
        if (opcionesCarrera[i].value === valorCarrera) {
            opcionesCarrera[i].selected = true;
        }
    }
});