$(document).ready(function() {
var paginas = [];
var paginaActual = 0;


// Obtén los datos de la API
$.get('https://tpig04empresas-production.up.railway.app/api/ofertas_estudiante', function(data) {
    console.log('Datos recibidos:', data);

    var elementosPorPagina = 5; // Cambia esto a cuántos elementos quieres por página
    datosMostrados = paginas;

    // Divide los datos en páginas
    for (var i = 0; i < data.ofertas.length; i += elementosPorPagina) {
        paginas.push(data.ofertas.slice(i, i + elementosPorPagina));
    }

    console.log('Páginas:', paginas);
 // Vacía el contenedor de paginación
    $('.pagination').empty();

 // Crea el botón "Previous"
    $('<li>')
      .addClass('page-item')
      .append(
        $('<a>')
          .addClass('page-link')
          .attr('href', '#')
          .text('Previous')
          .on('click', function() {
             
            console.log('Botón "Previous" clicado');
            if (paginaActual > 0) {
              console.log('Sin decremento= '+paginaActual);
              paginaActual--;
              
              console.log('Decrementando ='+paginaActual)  
              mostrarPagina(paginaActual);
            }else{
              console.log('pagina actual es menor a 0');
            }

          })
      )
     .appendTo('.pagination');

   // Crea los botones de paginación
   for (var i = 0; i < paginas.length; i++) {
    console.log('Creando botón para la página', i + 1);
    $('<li>')
        .addClass('page-item')
        .append(
            $('<a>')
                .addClass('page-link')
                .attr('href', '#')
                .text(i + 1)
                .on('click', (function(i) {
                    return function() {
                        console.log('Botón clicado para la página', i + 1);
                        paginaActual = i; // Actualiza la página actual
                        mostrarPagina(i);
                    };
                })(i))
        )
        .appendTo('.pagination');
}

// Crea el botón "Next"
$('<li>')
    .addClass('page-item')
    .append(
        $('<a>')
            .addClass('page-link')
            .attr('href', '#')
            .text('Next')
            .on('click', function() {
              if (paginaActual < paginas.length - 1) {
                paginaActual++;
                mostrarPagina(paginaActual );}
            })
    )
    .appendTo('.pagination');

// Muestra los datos de la primera página
mostrarPagina(0);
});

// Función para mostrar los datos de una página
function mostrarPagina(numeroPagina,datos=paginas) {
    console.log('Mostrando página', numeroPagina + 1);

    // Borra los datos actuales
    $('.api').empty();

    // Obtiene los datos de la página
  //var datosPagina = paginas[numeroPagina];
    var datosPagina = datos[numeroPagina];
    
    //si no hay datos en la pagina
    if(datosPagina.length==0){
      $('.api').append('<div class="text-center"><h1>No hay resultados</h1></div>');
    }
    // Deshabilita el botón "Previous" si estás en la primera página
    if (numeroPagina === 0) {
      $('.pagination .page-item:first-child').addClass('disabled');
  } else {
      $('.pagination .page-item:first-child').removeClass('disabled');
  }

  // Deshabilita el botón "Next" si estás en la última página
  if (numeroPagina === datos.length - 1) {
      $('.pagination .page-item:last-child').addClass('disabled');
  } else {
      $('.pagination .page-item:last-child').removeClass('disabled');
  }

    //si hay datos en la pagina
    // Muestra los datos de la página
    $.each(datosPagina, function(index, oferta) {
        // Crea una nueva tarjeta para cada empresa
        var newCard = $(
            // Aquí va el código HTML de la tarjeta
            '<div class="card mb-4" style="width: auto;" id="card'+index+'">' +
                  '<div class="card-body mb-4">' +
                    '<table class="table table-borderless">' +
                    '<tbody>' +
                       ' <tr>' +
                          '<td colspan="2">' +
                            '<h6 class="card-subtitle mb-2 text-muted">Se busca:</h5>' +
                              '<a class="sidebar-brand d-flex align-items-center">' +
                                '<div class="sidebar-brand-icon">' +
                                  '<img src="https://cdn-icons-png.flaticon.com/512/1063/1063376.png" width="30" />' +
                                '</div>' +
                                '<div class="sidebar-brand-text mx-2"><h5 >'+ oferta.carreras_solicitadas+'</h5></div>' +
                              '</a>' +
                            '<h6 class="card-subtitle mb-2 text-muted">Para:</h6>'+
                           ' <a class="sidebar-brand d-flex align-items-center">'+
                              '<div class="sidebar-brand-icon">'+
                                '<img src="https://cdn-icons-png.flaticon.com/512/1283/1283342.png" width="30" />'+
                              '</div>'+
                              '<div class="sidebar-brand-text mx-2 mb-2"><h5 id="cargo'+index+'" >'+oferta.puesto +'</h5></div>'+
                           ' </a>'+   
                           ' <a class="sidebar-brand d-flex align-items-center mb-2">'+
                              '<div class="sidebar-brand-icon mb-2">'+
                                '<img src="https://cdn-icons-png.flaticon.com/512/2830/2830596.png" width="20" />'+
                             '</div>'+
                              '<div class="sidebar-brand-text mx-2"><h6 class="card-subtitle text-muted" id="empresa'+index+'">'+oferta.nombre_empresa+'</h6></div>'+
                            '</a>'+
                            '<a class="sidebar-brand d-flex align-items-center mb-2">'+
                              '<div class="sidebar-brand-icon mb-2">'+
                                '<img src="https://cdn-icons-png.flaticon.com/512/1483/1483234.png" width="20" />'+
                              '</div>'+
                              '<div class="sidebar-brand-text mx-2"><h6 id="direccion'+index+'" class="card-subtitle text-muted">'+oferta.direccion+'</h6></div>'+
                            '</a>'+                
                           ' <a class="sidebar-brand d-flex align-items-center mb-2">'+
                              '<div class="sidebar-brand-icon mb-2">'+
                                '<img src="https://cdn-icons-png.flaticon.com/512/126/126509.png" width="20" />'+
                              '</div>'+
                              '<div class="sidebar-brand-text mx-2"><h6 class="card-subtitle text-muted">'+oferta.telefono+'</h6></div>'+
                           ' </a>'+
                            '<a class="sidebar-brand d-flex align-items-center mb-2">'+
                              '<div class="sidebar-brand-icon mb-2">'+
                                '<img src="https://cdn-icons-png.flaticon.com/512/2258/2258541.png" width="20" />'+
                             ' </div>'+
                              '<div class="sidebar-brand-text mx-2"><h6 class="card-subtitle text-muted">'+oferta.email+'</h6></div>'+
                            '</a>'+
                            '<a class="sidebar-brand d-flex align-items-center mb-2">'+
                              '<div class="sidebar-brand-icon mb-2">'+
                                '<img src="https://cdn-icons-png.flaticon.com/512/2492/2492300.png" width="20" />'+
                              '</div>'+
                             ' <div class="sidebar-brand-text mx-2"><h6 id="sueldo'+index+'" class="card-subtitle text-muted">'+oferta.salario+'</h6></div>'+
                            '</a>'+
                            '<h6 class="card-subtitle mb-2 text-muted">Fecha máxima para aplicar:</h6>'+
                            '<a class="sidebar-brand d-flex align-items-center mb-2">'+
                              '<div class="sidebar-brand-icon mb-2">'+
                               ' <img src="https://cdn-icons-png.flaticon.com/512/661/661512.png" width="20" />'+
                             ' </div>'+
                             ' <div class="sidebar-brand-text mx-2"><h6 class="card-subtitle">'+oferta.fecha_max_aplicar+'</h6></div>'+
                            '</a>'+
                            '<button id="aplicar'+index+'" type="button" class="btn btn-outline-success">Aplicar</button>'+
                          '</td>'+
                          '<td>'+
                           ' <a class="sidebar-brand d-flex align-items-center mb-2">'+
                             ' <div class="sidebar-brand-icon">'+
                               ' <img src="https://cdn-icons-png.flaticon.com/512/8915/8915968.png" width="30" />'+
                              '</div>'+
                              '<div class="sidebar-brand-text mx-2"><h5 class="card-subtitle  text-muted">Descripción:</h5></div>'+
                            '</a>'+
                           ' <h6 class="card-subtitle mb-2">'+oferta.descripcion_proyecto+'</h6>'+
                           ' <input type="hidden" id="idEmpresa'+index+'" value="'+oferta.id_empresa+'"></input>'+
                         ' </td>'+
                         ' <td>'+
                          '</td>'+
                        '</tr>'+
                      '</tbody>'+
                    '</table>'+
                 ' </div>'
            // Asegúrate de reemplazar los datos de la tarjeta con los datos de 'oferta'
        );

        // Añade la nueva tarjeta al contenedor
        $('.api').append(newCard);
    });
}

  // Escucha el evento 'input' en el campo de entrada
  $('#search').on('input', function() {
    // Obtiene el valor del campo de entrada
    var searchValue = $(this).val();

    // Filtra los datos basándote en el valor del campo de entrada
    var filteredData = [];
    
    for (var i = 0; i < paginas.length; i++) {
      filteredData.push(paginas[i].filter(function(oferta) {
        //filtrando por nombre de empresa.
        return oferta.name.toLowerCase().includes(searchValue.toLowerCase());
      }));
    }

    // Muestra los datos filtrados
    mostrarPagina(0, filteredData);
  });
   // Aquí va todo tu código JavaScript
});