$(document).ready(function($) {
		$('#mostrarVenta').dataTable({
			language: {
        			"decimal": "",
        			"emptyTable": "No se han realizado ventas",
        			"info": "",
        			"infoEmpty": "",
        			"infoFiltered": "(Filtrado de _MAX_ total ventas)",
        			"infoPostFix": "",
        			"thousands": ",",
        			"lengthMenu": "Mostrar _MENU_ Ventas",
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
});