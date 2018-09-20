function updateElementIndex(el, prefix, ndx) {
        var id_regex = new RegExp('(' + prefix + '-\\d+)');
        var replacement = prefix + '-' + ndx;
        if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
        if (el.id) el.id = el.id.replace(id_regex, replacement);
        if (el.name) el.name = el.name.replace(id_regex, replacement);
    }

function addForm(prefix, desc) {
    var formCount = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
    var crntIndex = formCount;
    var row = $('.dynamic-form:first').clone(true).get(0);
    console.log(desc);
    $(row).removeAttr('id').removeClass('hidden').insertAfter($('.dynamic-form:last')).children('.hidden').removeClass('hidden');
    //$(row).children().first().children("input[id$='mercaderia']").val("Hola");
    //console.log($(row).children().first().children().first().val());
    $(row).children().not(':last').children().each(function() {
        updateElementIndex(this, prefix, formCount);
        $(this).val('');
    });
    $(row).find('.delete-row').click(function() {
        deleteForm(this, prefix);
    });
    $('#id_' + prefix + '-TOTAL_FORMS').val(formCount + 1);
    $("#id_form-" + crntIndex + "-mercaderia").val(desc);
    return false;
}

function deleteForm(btn, prefix) {
    $(btn).parents('.dynamic-form').remove();
    var forms = $('.dynamic-form');
    $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
    for (var i=0, formCount=forms.length; i<formCount; i++) {
        $(forms.get(i)).children().not(':last').children().each(function() {
            updateElementIndex(this, prefix, i);
        });
    }
    return false;
}