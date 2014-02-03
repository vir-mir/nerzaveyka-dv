/**
 *
 * @param data
 * {
 *     body:
 *     form_attr:
 *     head:
 *     button: {
 *         attr:
 *         class:
 *         name:
 *     }
 * }
 */
function show_model(data) {


    var html = '<div id="myModal" class="modal hide fade" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">';

    if (data.head!==undefined && data.head!==null && data.head!=='' && data.head!==false) {

        html += '<div class="modal-header">' +
            '<button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>' +
            '<h3 id="myModalLabel">' +
            data.head +
            '</h3>' +
            '</div>';
    }


    html += "<form"+data.form_attr+">"

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

    html += '</form>'

    html += '</div>';

    if ($("#myModal").size() > 0) {
        $("#myModal").remove();
    }

    $('body').append(html);
    $("#myModal").modal();


}



var curent = 1;

function slide(obj) {
    $('.gallery-men-item').removeClass('act');
    obj.addClass('act');
    var id = obj.attr('id').replace(/[\w]+\-/i, '')
    $('.gallery-content').removeClass('act').slideUp(500);
    curent = id
    $('#g-'+id).addClass('act').stop(false, false).show(500);

    return false;
}

function forSlide() {

    var timeLine = 5;
    var start = 1;
    curent = start;
    var end = $('.gallery-men-item').size();

    setInterval(function () {
        curent++;
        if (end < curent) curent = start;
        slide($('#gitem-'+curent));
    }, timeLine*1000);

    return false;
}

var body_fos = null
var callback_click = null

$(function () {

    $('.gallery-men-item').click(function () { return slide($(this)) });
    //forSlide();

    $('body').tooltip({
        selector: ".tooltips"
    });

    $('.fos_click').click(function () {

        if (!body_fos) {
            body_fos = $('#body_fos').html()
            $('#body_fos').remove()
        }

        var data = {
            'head': "Задать вопрос",
            'body': body_fos,
            'form_attr': ' method="post" class="form_fos" action="/feedback/ajax/?function_event=send_fos" style="margin: 0"',
            'button': [
                {name: 'Отправить', attr:'type="submit" name="send_fos"', class:'btn-primary'}
            ]
        };

        show_model(data);


        $('.form_fos').submit(function () {
            $.post('/feedback/ajax/?function_event=send_fos', $(this).serialize(), function (data) {
                $('.notifications').remove()
                $('body').prepend('<div class="notifications top-right"></div>');
                $.each(data.text, function (i,v) {
                    $('.top-right')
                        .notify({
                            message: v,
                            type: data.style
                        })
                        .show();
                });

                if (data.error==1) {
                    $('.modal-header button').click();
                }

            }, 'json')
            return false;
        });


        return false;
    });

    $('.callback_click').click(function () {

        if (!callback_click) {
            callback_click = $('#callback_click').html()
            $('#callback_click').remove()
        }

        var data = {
            'head': "Обратный звонок",
            'body': callback_click,
            'form_attr': ' method="post" class="form_callback" action="/feedback/ajax/?function_event=send_callback" style="margin: 0"',
            'button': [
                {name: 'Отправить', attr:'type="submit" name="send_callback"', class:'btn-primary'}
            ]
        };

        show_model(data);


        $('.form_callback').submit(function () {
            $.post('/feedback/ajax/?function_event=send_callback', $(this).serialize(), function (data) {
                $('.notifications').remove()
                $('body').prepend('<div class="notifications top-right"></div>');
                $.each(data.text, function (i,v) {
                    $('.top-right')
                        .notify({
                            message: v,
                            type: data.style
                        })
                        .show();
                });

                if (data.error==1) {
                    $('.modal-header button').click();
                }

            }, 'json')
            return false;
        });


        return false;
    });

    $("a[href$='.jpg'], a[href$='.png'], a[href$='.gif'], a[href$='.jpeg'], .lightbox").lightBox();

    $('.all_services').click(function () {

        $(this).prev().find('li.hidden').removeClass('hidden');
        $(this).slideUp(300)

        return false;
    });

});