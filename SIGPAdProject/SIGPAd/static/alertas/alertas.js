
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
  $("#alerta").click(function(event) {
    var pdf = new jsPDF('p', 'pt', 'letter');
    html = $("#pdf").html();
    specialElementHandlers = {};
    margins = {top: 15,bottom: 15,left: 15,width: 170};    
    pdf.fromHTML(html, 15,15, {'width': 170},function (dispose) {pdf.save('prueba.pdf');}, margins);
  });
})

