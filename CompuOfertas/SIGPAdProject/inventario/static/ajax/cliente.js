$(document).ready(function($) {
	$.ajax({
		url: 'clienteRegistrado/',
		type: 'GET',
		cache: false,		
	})
	.done(function(resp) {		        
		for(let i=0;i<resp.length;i++){
			var elemento = resp[i].fields;
            let user = elemento.usuario[0];            
			var usuario = `<option>${user}</option>`
			$('#select-js').append(usuario)
		}
		$('#select-js').select2({
    		placeholder: "Seleccione un cliente",
   			allowClear: true
		});		
	})
	.fail(function() {
		console.log("error");
	})	
});