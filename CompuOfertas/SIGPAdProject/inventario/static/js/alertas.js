
$(document).ready(function(){
  $("#salir").click(function(event) {
    
    swal({
      title: 'Está Seguro que desea salir?',      
      type: 'warning',
      showCancelButton: true,
      confirmButtonText: 'Si,salir!',
      cancelButtonText: 'No, cancelar!',
      reverseButtons: true
    }).then((result) => {
      if(result.value)
      {        
        window.location.href = "/logout";        
      }      
    })
  });
});


$(document).ready(function(){
  var doc = new jsPDF('l','pt','a4');
  var specialElementHandlers = {
    '#editor': function (element, renderer) {
        return true;
    }
};
  $("#alerta").click(function(event) {
    doc.text(20,20,'Planilla de Pago');
    doc.fromHTML($('#pdf').tableExport,15,15,{ 
      'width':170,
      'elementHandlers': specialElementHandlers});    
    doc.save('prueba2.pdf')})
    
})

$(document).ready(function(){  
  if($("#creacion").length > 0)
    { 
      var texto = $("#creacion").html()     
      swal(texto,' ','success');
    }
  
})

$(document).ready(function(){
  if($("#crearError".length >0 ))
    swal($("#crearError").html(),' ', 'error');
})

$(document).ready(function(){
  if($("#crearPuesto").length > 0)
    swal($("#crearPuesto").html(),' ','success');
})

$(document).ready(function(){
  if($("#errorPuesto".length >0))    
    swal($("#errorPuesto").html(),' ','error');
})

$(document).ready(function(){
  if($("#crearEmpleado").length > 0)
    swal($("#crearEmpleado").html(), '', 'success');
})



