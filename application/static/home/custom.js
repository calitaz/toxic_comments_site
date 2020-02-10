$('document').ready(function(){
   
    $("#toxicbtn").click(function(){
        var id = $("#commentid").val();

        $.ajax({
            url: '/toxic_comment',
            type: 'POST',
            data: JSON.stringify({ "id" : id } ),
            dataType: 'json',
            contentType: 'application/json; charset=utf-8',
            success: function (data, result){
                if(result == 'success'){
                    console.log(JSON.stringify(data))
                    Swal.fire({
                        title: 'Obrigado!',
                        text: data.msg,
                        icon: 'success',
                        confirmButtonText: 'Ok'
                    }).then(function(){
                        window.location.reload();
                    });
                } else {
                    Swal.fire({
                        title: 'Ooops',
                        text: 'Algo de errado aconteceu',
                        icon: 'error'
                    })
                }
            },
            error: function (event, jqxhr, settings, thrownError){
                console.log('event: ' + JSON.stringify(event));
                console.log('jqxhr: ' + jqxhr);
                console.log('settings: ' + settings);
                console.log('thrownError: ' + thrownError);
            }
        })
    });

    $("#nontoxicbtn").click(function(){
        var id = $("#commentid").val();

        $.ajax({
            url: '/nontoxic_comment',
            type: 'POST',
            data: JSON.stringify({ "id" : id } ),
            dataType: 'json',
            contentType: 'application/json; charset=utf-8',
            success: function (data, result){
                if(result == 'success'){
                    Swal.fire({
                        title: 'Obrigado!',
                        text: data.msg,
                        icon: 'success',
                        confirmButtonText: 'Ok'
                    }).then(function(){
                        window.location.reload();
                    });
                } else {
                    Swal.fire({
                        title: 'Ooops',
                        text: 'Algo de errado aconteceu',
                        icon: 'error'
                    })
                }
            },
            error: function (event, jqxhr, settings, thrownError){
                console.log('event: ' + JSON.stringify(event));
                console.log('jqxhr: ' + jqxhr);
                console.log('settings: ' + settings);
                console.log('thrownError: ' + thrownError);
            }
        })
    });


});