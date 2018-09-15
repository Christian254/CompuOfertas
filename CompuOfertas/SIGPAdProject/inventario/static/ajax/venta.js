$(document).ready(function() {
	$.ajax({
		url: 'productoDisponible/', //Servicio con los productos con existencia > 0
		type: 'GET',
		dataType: 'json',
        cache: false,
	})
	.done( function(resp) {
		/*Iterando el JSON y agregando la fila a la tabla*/
        $('form').append(`<input name="cantidad" type="text" value="${resp.length}" hidden>`)        
		for(let i=0;i<resp.length;i++){
			var elemento = resp[i].fields;                       
			var producto = `<tr">`
            producto += `<td><input type="text" name="codigo-${i+1}" value="${elemento.codigo}" hidden>${elemento.codigo}</td>`			
			producto +=	`<td>${elemento.nombre}</td>`
			producto +=	`<td>${elemento.marca}</td>`
            producto += `<td>${elemento.inventario[1]}</td>`
			producto +=	`<td>${elemento.inventario[0]}</td>`
			producto +=	`<td ><a name="${resp[i].pk}" class="agregar"><span class="glyphicon glyphicon-ok text-success" aria-hidden="true"></span></a></td>`
			producto +=	'</tr>'
			$('#productoDisponible').append(producto)
		}
		var tablaVenta = $('#tablaVenta').DataTable({ //Usando el plugin DataTable
			 responsive: true,             
             "paging":         false,
             lengthMenu: [[-1],["Todos"]],
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
    			},                 
		});	
		var tabla = $('#tablaProducto').DataTable({
            responsive: true, 
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
        $('#productosCantidad').val(tablaVenta.rows().count());
		agregarProducto(tabla,tablaVenta); //Funcion Para agregar producto a la tablaVenta
		quitarProducto(tablaVenta,tabla); //Funcion Para quitar el producto de la tablaVenta
		validarCantidad(tablaVenta); //Funcion para validar que la cantidad a vender sea menor o igual a la existencia
		descuento(tablaVenta);
        })
	.fail(function() {
		console.log("error");
	})
})
	


