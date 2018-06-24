
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

