$(function() {
	$.ajax({
		url: 'productoDisponible/',
		type: 'GET',
		dataType: 'json',
	})
	.done(function(resp) {		
		resp.forEach( function(prop,index) {
			var elemento = prop.fields			
			var producto = '<tr>'
			producto +=	`<td>${elemento.nombre}</td>`
			producto +=	`<td>${elemento.marca}</td>`
			producto +=	`<td>${elemento.existencia}</td>`
			producto +=	`<td><button id="${prop.pk}" class="btn btn-primary">Añadir</button></td>`
			producto +=	'</tr>'
			$('#productoDisponible').append(producto)
		});	
		$('table').DataTable({
			 lengthMenu: [[1,5,10,-1],["1","5","10","Todos"]],
    language: {
        "decimal": "",
        "emptyTable": "No hay información",
        "info": "",
        "infoEmpty": "Mostrando 0 to 0 of 0 Entradas",
        "infoFiltered": "(Filtrado de _MAX_ total entradas)",
        "infoPostFix": "",
        "thousands": ",",
        "lengthMenu": "Mostrar _MENU_ Entradas",
        "loadingRecords": "Cargando...",
        "processing": "Procesando...",
        "search": "Buscar:",
        "zeroRecords": "Sin resultados encontrados",
        "paginate": {
            "first": "Primero",
            "last": "Ultimo",
            "next": "Siguiente",
            "previous": "Anterior"
        }
    },
    
});	
	})
	.fail(function() {
		console.log("error");
	})
	
})