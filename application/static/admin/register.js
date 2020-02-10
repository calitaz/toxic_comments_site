$(document).ready(function(){

    $('form').validate({
        errorClass: "has-danger",
        validClass: "has-success",
        rules: {
            name: {
                required: true
            },
            username: {
                required: true,
                minlength: 4
            },
            email: {
                required: true,
                email: true
            },
            password: {
                required: true,
                minlength: 6
            },
            confirmpassword: {
                equalTo: "#password"
            }
        },
        messages: {
            name: "O nome é obrigatório",
            username: {
                required: "Usuário é obrigatório",
                minlength: "Usuário deve conter ao menos 4 caracteres"
            },
            email: {
                required: "Email é obrigatório",
                email: "Email invalido (ex: email@email.com)"
            },
            password: {
                required: "Digite sua senha",
                minlength: "A senha deve possui ao menos 6 caracteres"
            },
            confirmpassword: {
                equalTo: "Senhas não conferem"
            }
        },
        submitHandler: function (form, event) {
            var csrftoken = $('meta[name=csrf-token]').attr('content')
            event.preventDefault();
            $.ajaxSetup({
                beforeSend: function(xhr, settings) {
                    if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", "{{ form.csrf_token._value() }}")
                    }
                }
            })
            $.ajax({
                url: "register/create",
                method: 'POST',
                data:  $('form').serialize(),
                success: function (data, result) {
                    console.log(data);
                    if(data.status == "true"){
                        Swal.fire({
                            title: 'Cadastrado com sucesso!',
                            text: data.msg,
                            icon: 'success',
                            confirmButtonText: 'Ok'
                        }).then(function(){
                            window.location.href = "/admin/login";
                        });
                    }else{
                        Swal.fire({
                            title: 'Ooops',
                            text: data.msg,
                            icon: 'error'
                        });
                    }
                },
                error: function (error, textStatus, errorThrown) {
                    Swal.fire({
                        icon: 'error',
                        title: 'Oops...',
                        text: 'Alguma coisa deu errado, entre em contato com a equipe de suporte.'
                    });
                }
            })
        }
    })
});