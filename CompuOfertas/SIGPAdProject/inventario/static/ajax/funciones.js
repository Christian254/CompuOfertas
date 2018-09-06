function agregarProducto(tabla,tablaVenta){
	$('#tablaProducto tbody').on( 'click', '.agregar', function () {
    	let fila = tabla.row( $(this).parents('tr') );
    	let productoDatos = tabla.row( $(this).parents('tr') ).data();
    	console.log(productoDatos);
        fila.remove();
        tabla.draw();
        tablaVenta.row.add(
        	[productoDatos[0], 
        	productoDatos[1],productoDatos[2],'<input class="cantidad" value="1" type="number" step="1" style="width:75px;">','<button type="button" class="btn btn-danger quitar">Quitar</button>']).draw();			
		});
}

function quitarProducto(tablaVenta,tabla){
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
}
function validarCantidad(tablaVenta){
	$('#tablaVenta tbody').on('keyup','input', function () {    	
    	let productoDatos = tablaVenta.row( $(this).parents('tr') ).data();
    	let existencia = parseInt(productoDatos[2]);
    	let cantidad = $(this).val();     	 	
    	if( cantidad > existencia || cantidad < 1){
    		console.log('invalido');
    		$(this).attr('style', 'border: 2px solid red; width:75px');
    		$('#botonVender').prop('disabled', 'true');
    	}   
    	else{    		
    		console.log('valido');
    		$(this).attr('style', 'width:75px');
    		$('#botonVender').removeAttr('disabled');
    	} 	  	      			
		});
}
