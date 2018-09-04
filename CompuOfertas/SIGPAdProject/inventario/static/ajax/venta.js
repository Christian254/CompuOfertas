$(document).ready(function() {
	$.ajax({
		url: 'productoDisponible/',
		type: 'GET',
		dataType: 'json',
	})
	.done( function(resp) {
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
		var tablaVenta = $('#tablaVenta').DataTable({
			 lengthMenu: [[2,5,7,-1],["2","5","7","Todos"]],
    			language: {
        			"decimal": "",
        			"emptyTable": "Seleccione los productos a vender",
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
		var tabla = $('#tablaProducto').DataTable({
			 lengthMenu: [[2,5,7,-1],["2","5","7","Todos"]],
    			language: {
        			"decimal": "",
        			"emptyTable": "No hay productos para vender",
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
		$('#tablaProducto tbody').on( 'click', '.agregar', function () {
    	let fila = tabla.row( $(this).parents('tr') );
    	let productoDatos = tabla.row( $(this).parents('tr') ).data();
    	console.log(productoDatos);
        fila.remove();
        tabla.draw();
        tablaVenta.row.add(
        	[productoDatos[0], 
        	productoDatos[1],productoDatos[2],'<input type="text">','<button type="button" class="btn btn-danger quitar">Quitar</button>']).draw();			
		});
		$('#tablaVenta tbody').on( 'click', '.quitar', function () {
    	let fila = tablaVenta.row( $(this).parents('tr') );
    	let productoDatos = tablaVenta.row( $(this).parents('tr') ).data();
    	console.log(productoDatos);
        fila.remove();
        tablaVenta.draw();
        tabla.row.add(
        	[productoDatos[0], 
        	productoDatos[1],productoDatos[2],'<button type="button" class="agregar btn btn-primary">Añadir</button>']).draw();			
		});
		})
	.fail(function() {
		console.log("error");
	})
})
	


