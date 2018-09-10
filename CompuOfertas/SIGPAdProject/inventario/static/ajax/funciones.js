function agregarProducto(tabla,tablaVenta){
	$('#tablaProducto tbody').on( 'click', '.agregar', function () {
    	let fila = tabla.row( $(this).parents('tr') );
    	let productoDatos = tabla.row( $(this).parents('tr') ).data();    	
        fila.remove();
        tabla.draw();
        dato=productoDatos[0].split('-')[1].split('"')[0]; //para asignar el name
        console.log(dato);
        tablaVenta.row.add(
        	[productoDatos[0], 
        	productoDatos[1],productoDatos[2],productoDatos[3],productoDatos[4],`<input name="cantidad-${dato}" class="cantidad" value="1" type="number" step="1" style="width:75px;" min="1" max="${productoDatos[4]}">`,'<button type="button" class="btn btn-danger quitar">Quitar</button>']).draw();			
		});
}

function quitarProducto(tablaVenta,tabla){
	$('#tablaVenta tbody').on( 'click', '.quitar', function () {
    	let fila = tablaVenta.row( $(this).parents('tr') );
    	let productoDatos = tablaVenta.row( $(this).parents('tr') ).data();
        fila.remove();
        tablaVenta.draw();
        tabla.row.add(
        	[productoDatos[0], 
        	productoDatos[1],productoDatos[2],productoDatos[3],productoDatos[4],'<button type="button" class="agregar btn btn-primary">Añadir</button>']).draw();			
		deshabilitarVenta();
		});
	
}
function validarCantidad(tablaVenta){
	$('#tablaVenta tbody').on('click keyup','input', function () {    	
    	let productoDatos = tablaVenta.row( $(this).parents('tr') ).data();
    	let existencia = parseInt(productoDatos[4]);
    	let cantidad = $(this).val();     	  	   	 	
    	if( cantidad > existencia || cantidad < 1){
    		$(this).attr('class', 'invalido');
    		$(this).attr('style', 'border: 2px solid red; width:75px');  			
    	}   
    	else{   		
    		$(this).attr('style', 'width:75px');
    		$(this).removeAttr('class');   		
    	} 
    	deshabilitarVenta();
    	});	 
}
function deshabilitarVenta(){
	error = $('input').filter($('.invalido')).length;    	
    	if(error>0){
    		$('#botonVender').prop('disabled', 'true');
    	}
    	else{
    		$('#botonVender').removeAttr('disabled'); 
    	}   	 	      			
}
