    $(document).ready(function() {
        var pagMax = $('.numPag').length;
        var actual = $('.numPag').attr('val');
        $('#anterior-pag').prop('disabled', true);
        let remover = () => {
            $('.numPag').each(function() {
                $(this).removeClass('active');
            });
        }
        $('#siguiente-pag').click(function(e) {
            let param = $('#siguiente-pag').attr('href');
            console.log(param);
            actual++;
            e.preventDefault();
            if (actual == pagMax) {
                $('#siguiente-pag').removeAttr('href');
                $('#siguiente-pag').prop('disabled', true);
            } else {
                $('#siguiente-pag').prop('disabled', false);
            }
            $.ajax({
                url: param,
                type: 'GET',
                dataType: "html",
                success: function(data) {
                    remover();
                    console.log(actual);
                    $('.numPag').eq(actual - 1).addClass('active')
                    console.log($(data).find('.table').html());
                    $('.table').html($(data).find('.table').html());
                    $('#siguiente-pag').attr('href', $(data).find('#siguiente-pag').attr('href'));
                    $('#anterior-pag').attr('href', $(data).find('#anterior-pag').attr('href'));
                    $('#anterior-pag').prop('disabled', false);
                },
            })
        });
        $('#anterior-pag').click(function(e) {
            let param = $('#anterior-pag').attr('href');
            actual--;
            if (actual < pagMax) {
                $('#siguiente-pag').prop('disabled', false);
            }
            if (actual == 1) {
                $('#anterior-pag').prop('disabled', true);
            }
            e.preventDefault();
            $.ajax({
                url: param,
                type: 'GET',
                success: function(data) {
                    remover();
                    $('.numPag').eq(actual - 1).addClass('active');
                    $('#anterior-pag').removeAttr('href');
                    $('.table').html($(data).find('.table').html());
                    $('#siguiente-pag').attr('href', $(data).find('#siguiente-pag').attr('href'));
                    $('#anterior-pag').attr('href', $(data).find('#anterior-pag').attr('href'));
                },
            })
        });
        $('.numPag').click(function(e) {
            numSig = Number($('a', this).text()) + 1;
            actual = numSig - 1;
            if (numSig >= pagMax) {
                numSig = pagMax;
            }
            console.log(actual);
            if (actual == 1) {
                $('#anterior-pag').prop('disabled', true);
            }
            if (actual >= 2) {
                $('#anterior-pag').prop('disabled', false);
            }
            if (actual == pagMax) {
                $('#siguiente-pag').prop('disabled', true);
            }
            if (actual < pagMax) {
                $('#siguiente-pag').prop('disabled', false);
            }
            console.log(actual);
            remover();
            e.preventDefault();
            $(this).addClass("active");
            url = $('a', this).attr('href');
            posicion = url.split('=')
            if (posicion[1] == pagMax) {
                $('#siguiente-pag').removeAttr('href');
            }
            $.ajax({
                url: url,
                type: 'GET',
                success: function(data) {
                    $('.table').html($(data).find('.table').html());
                    $('#siguiente-pag').attr('href', $(data).find('#siguiente-pag').attr('href'));
                    $('#anterior-pag').attr('href', $(data).find('#anterior-pag').attr('href'));
                    if (actual == 1) {
                        $('#anterior-pag').prop('disabled', true);
                        $('#anterior-pag').attr('href', $(data).find('#anterior-pag').removeAttr('href'))
                    }
                }
            })
        });
        $('#buscar').click(function(e) {
            e.preventDefault();
            url= `ingresarProducto?consulta=${$('#consulta').val()}`;
            $.ajax({
                url: url,
                type: 'GET',
                dataType: 'html',                      
            })
            .done(function(resp) {
                $('.table').html($(resp).find('.table').html());
                $('.pagination').html($(resp).find('.pagination').html());
                
            })
            .fail(function() {
                console.log("error");
            })
            .always(function() {
                console.log("complete");
            });
            
        });
    })
