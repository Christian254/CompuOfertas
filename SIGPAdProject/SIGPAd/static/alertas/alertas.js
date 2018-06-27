
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

