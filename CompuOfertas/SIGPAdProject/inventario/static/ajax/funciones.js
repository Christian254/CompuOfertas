function agregarProducto(tabla,tablaVenta){
	$('#tablaProducto tbody').on( 'click', '.agregar', function () {
    	let fila = tabla.row( $(this).parents('tr') );
    	let productoDatos = tabla.row( $(this).parents('tr') ).data();    	
        fila.remove();
        tabla.draw();
        dato=productoDatos[0].split('-')[1].split('"')[0]; //para asignar el name
        tablaVenta.row.add(
        	[productoDatos[0], 
        	productoDatos[1],productoDatos[2],productoDatos[3],productoDatos[4],`<input class="cantidad" id="cantidad-${dato}" name="cantidad-${dato}" value="1" type="number" step="1" style="width:75px;" min="0" max="${productoDatos[4]}">`,`<input id="descuento-${dato}" class="descuento" value="0" name="descuento-${dato}" type="number" step="0.01" min="0.00" max="1.00" style="width:75px;">`,`<input type="number" id="total-${dato}" style="width:75px;" disabled="true" value="${productoDatos[3]}">`,'<a class="quitar"><span class="glyphicon glyphicon-remove text-danger" aria-hidden="true"></span></a>']).draw();			
		$('#productosCantidad').val(tablaVenta.rows().count());
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
        	productoDatos[1],productoDatos[2],productoDatos[3],productoDatos[4],'<a class="agregar"><span class="glyphicon glyphicon-ok text-success" aria-hidden="true"></span></a>']).draw();			
		deshabilitarVenta();
		$('#productosCantidad').val(tablaVenta.rows().count());
        });
	
}
function validarCantidad(tablaVenta){
	$('#tablaVenta tbody').on('click keyup','.cantidad', function () {
        $(this).attr('class', 'cantidad');        	
    	let productoDatos = tablaVenta.row( $(this).parents('tr') ).data();
    	let existencia = parseInt(productoDatos[4]);
    	let cantidad = parseInt($(this).val());
        let dato=productoDatos[0].split('-')[1].split('"')[0]   	  	   	 	
    	if( cantidad > existencia || cantidad < 0 || isNaN(cantidad)){
    		$(this).addClass('invalido')
    		$(this).attr('style', 'border: 2px solid red; width:75px');
            $('#total-' + dato).text('');  			
    	}   
    	else{  		
    		$(this).attr('style', 'width:75px');
    		$(this).removeClass('invalido');
            let precio_unitario = parseFloat(productoDatos[3]);
            $('#total-' + dato).val(precio_unitario*cantidad);
            let descuento = $('#descuento-'+dato).val()            
            let descontado = parseFloat(precio_unitario*cantidad - precio_unitario*cantidad*descuento);
            descontado = descontado.toFixed(2);            
            $('#total-'+dato).val(descontado);             
    	} 
    	deshabilitarVenta();
    	});	 
}

function descuento(tablaVenta){
    $('#tablaVenta tbody').on('click keyup','.descuento', function () {
        $(this).attr('class', 'descuento');
        let productoDatos = tablaVenta.row( $(this).parents('tr') ).data()
        dato=productoDatos[0].split('-')[1].split('"')[0]  
        precio_unitario = parseFloat(productoDatos[3]);
        cantidad = parseInt($('#cantidad-'+dato).val())
        descuento =parseFloat($(this).val());        
        if(descuento < 0 || descuento > 1 || isNaN(descuento)){
            $(this).addClass('invalido')
            $(this).attr('style', 'border: 2px solid red; width:75px');
            $('#total-' + dato).text('');  
        }
        else{
            $(this).attr('style', 'width:75px');
            $(this).removeClass('invalido');
            let descontado = parseFloat(precio_unitario*cantidad - precio_unitario*cantidad*descuento); 
            descontado = descontado.toFixed(2);                
            $('#total-'+dato).val(descontado);
        }
       deshabilitarVenta()            
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
