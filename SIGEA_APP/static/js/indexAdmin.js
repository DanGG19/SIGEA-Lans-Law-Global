function confirmDelete(event, url) {
    event.preventDefault();
    Swal.fire({
        title: '¿Estás seguro?',
        text: "No podrás revertir esto!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Sí, borrar!'
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = url;
        }
    })
}


$(document).ready(function(){
    $('input[name="q"]').on('keyup', function(){
        var query = $(this).val();
        $.ajax({
            url: '/index-admin/',  // URL de la vista que maneja la búsqueda
            data: {
                'q': query  // Término de búsqueda
            },
            dataType: 'json',
            success: function(data){
                // Vacía la tabla
                $('#estudiantes_datos tbody').empty();
                console.log(data);
                // Itera sobre los resultados de búsqueda
                $.each(data, function(index, estudiante){
                    // Crea una nueva fila para cada estudiante
                    var newRow = $('<tr>');
                    newRow.append('<td>' + estudiante.id + '</td>');
                    newRow.append('<td>' + estudiante.first_name + '</td>');
                    newRow.append('<td>' + estudiante.last_name + '</td>');
                    newRow.append('<td>' + estudiante.username + '</td>');
                    newRow.append('<td>' + estudiante.email + '</td>');
                    newRow.append('<td>' + estudiante.sexo + '</td>');
                    newRow.append('<td>' + estudiante.genero + '</td>');
                    newRow.append('<td>' + estudiante.telefono + '</td>');
                    newRow.append('<td>' + estudiante.nacimiento + '</td>');
                    //para las acciones
                    newRow.append('<td><a href="/editarEstudiante/' + estudiante.pk + '" class="btn btn-primary"><i class="fas fa-edit"></i></a> <a href="/eliminarEstudiante/' + estudiante.pk + '" class="btn btn-danger delete-btn"><i class="fas fa-trash-alt"></i></a></td>');                    

                    // Añade la nueva fila a la tabla
                    $('#estudiantes_datos tbody').append(newRow);

                    $('.delete-btn').on('click', function(event) {
                        var url = $(this).attr('href');
                        confirmDelete(event, url);
                    });
                });
            }
        });
    });
});