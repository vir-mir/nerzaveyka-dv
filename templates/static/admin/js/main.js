function toggleButton() {
    $('.toggle-button').bootstrapSwitch();
}

function setdatetimepicker() {
    $('.datetimepicker').datetimepicker();
}

function wysihtml5Cut() {
    $('.wysihtml5Cut').wysihtml5({cut: true});
}

function validateForm(name) {
    $('.'+name).validate();
}

/**
 *
 * @param data
 * {
 *     body:
 *     form:
 *     head:
 *     button: {
 *         attr:
 *         class:
 *         name:
 *     }
 * }
 */
function show_model_admin(data) {


    var html = '<div id="myModal" style="width: 900px;left: 50%;margin-left: -450px;" class="modal hide fade" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">';

    if (data.head!==undefined && data.head!==null && data.head!=='' && data.head!==false) {

        html += '<div class="modal-header">' +
            '<button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>' +
            '<h3 id="myModalLabel">' +
            data.head +
            '</h3>' +
            '</div>';
    }

    html += '<form action="?" style="margin: 0" method="post" enctype="multipart/form-data" class="'+data.form+'">'

    if (data.body!==undefined && data.body!==null && data.body!=='' && data.body!==false) {

        html += '<div class="modal-body">' +
            data.body +
            '</div>';
    }

    html += '<div class="modal-footer">';

    if (data.button!==undefined && data.button!==null && data.button!=='' && data.button!==false) {

        $.each(data.button, function (i,v) {
            html += '<button '+v.attr+' class="btn '+v.class+'">'+v.name+'</button>';
        });

    }

    html += '<button class="btn" data-dismiss="modal">Закрыть</button>' +
        '</div>';

    html += "</form>";

    html += '</div>';

    if ($("#myModal").size() > 0) {
        $("#myModal").remove();
        $(".modal-backdrop").remove();
    }

    $('body').append(html);


}

function ajaxForm(button, title, model, function_event) {

    $('.'+function_event).submit(function () {
        var data_attr = $('.'+function_event).serialize()


        $.post('/'+model+'/ajax/', data_attr, function (data) {
            allAjaxFunction(title,function_event,data,button,model)
        });

        return false;
    });



}

function errors_show() {
    if (errors) {
        $.each(errors.messages, function (i,v) {
            $('.top-right')
                .notify({
                    message: { text: v },
                    type: errors.style
                })
                .show();
        });
    }

}


function allAjaxFunction(title,function_event,data,button,model) {
    show_model_admin({head: title, form:function_event, body:data, button: eval(button)});
    toggleButton();
    wysihtml5Cut();
    validateForm(function_event);
    ajaxForm(button, title, model,function_event);
    InitUploadifyQueue();
    $('#myModal').modal('show')
    errors_show();
    load()
}

function load() {
    $('.admin_button').unbind('click');
    $('.portfolio').unbind('click');
    $('.admin_button_set').unbind('click');
    $('.img-admin').unbind('hover');


    $('.portfolio').click(function () {
        if ($(this).parent().hasClass('active')) {
            $(this).parent().removeClass('active')
        } else {
            $(this).parent().addClass('active')
        }

        $('#portfolios').val(portfolios_active())
        return false;
    })

    $('.admin_button').click(function () {
        var id = $(this).attr('id').split('-');
        var title = $(this).attr('data-original-title');
        var button = $(this).attr('data-button');
        var model = id[0]
        var event_data = id[1].split(':')
        var function_event = event_data[0]
        if (event_data.length == 2) {
            id = event_data[1]
        } else {
            id = 0
        }
        $.get('/'+model+'/ajax/', {function_event: function_event, id:id}, function (data) {
            allAjaxFunction(title,function_event,data,button,model)
        })


        return false;
    });


    $('.img-admin').hover(function () {
        $('>.aply', this).find('a').removeClass('hidden')
    }, function () {
        $('>.aply', this).find('a').addClass('hidden')
    });

    $('.admin_button_set').click(function () {

        if (!confirm("Вы уверены в своих действиях?")) return false;

        var model = $(this).attr('model');
        var function_event = $(this).attr('function_event');
        var id = $(this).attr('id');

        $.get('/'+model+'/ajax/', {function_event: function_event, id:id}, function (data) {
            $('.top-right')
                .notify({
                    message: { text: data.text },
                    type: data.style
                })
                .show();
        }, 'json')

        return false;

    });

}



function portfolios_active() {
    var text = ''

    $('.portfolios.active a').each(function () {
        text += $(this).attr('id').replace(/portfolio_/, '') + ','
    });

    return text

}


$(function () {

    load()

})