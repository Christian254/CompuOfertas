$(document).ready(function() {
	$.ajax({
		url: 'productoDisponible/', //Servicio con los productos con existencia > 0
		type: 'GET',
		dataType: 'json',
	})
	.done( function(resp) {
		/*Iterando el JSON y agregando la fila a la tabla*/
		for(let i=0;i<resp.length;i++){
			var elemento = resp[i].fields;
			var producto = `<tr id="fila${i}">`			
			producto +=	`<td>${elemento.nombre}</td>`
			producto +=	`<td>${elemento.marca}</td>`
			producto +=	`<td>${elemento.existencia}</td>`
			producto +=	`<td><button name="${resp[i].pk}" class="agregar btn btn-primary">Añadir</button></td>`
			producto +=	'</tr>'
			$('#productoDisponible').append(producto)
		}
		var tablaVenta = $('#tablaVenta').DataTable({ //Usando el plugin DataTable
			 lengthMenu: [[2,5,7,-1],["2","5","7","Todos"]],
    			language: {
        			"decimal": "",
        			"emptyTable": "Seleccione los productos a vender",
        			"info": "",
        			"infoEmpty": "",
        			"infoFiltered": "(Filtrado de _MAX_ total productos)",
        			"infoPostFix": "",
        			"thousands": ",",
        			"lengthMenu": "Mostrar _MENU_ Productos",
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
		var tabla = $('#tablaProducto').DataTable({
			 lengthMenu: [[2,5,7,-1],["2","5","7","Todos"]],
    			language: {
        			"decimal": "",
        			"emptyTable": "No hay productos para vender",
        			"info": "",
        			"infoEmpty": "",
        			"infoFiltered": "(Filtrado de _MAX_ total Productos)",
        			"infoPostFix": "",
        			"thousands": ",",
        			"lengthMenu": "Mostrar _MENU_ Productos",
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
		agregarProducto(tabla,tablaVenta); //Funcion Para agregar producto a la tablaVenta
		quitarProducto(tablaVenta,tabla); //Funcion Para quitar el producto de la tablaVenta
		validarCantidad(tablaVenta); //Funcion para validar que la cantidad a vender sea menor o igual a la existencia
		})
	.fail(function() {
		console.log("error");
	})
})
	


