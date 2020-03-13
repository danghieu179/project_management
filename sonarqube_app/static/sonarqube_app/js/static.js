(function ($) {
    $.fn.inputFilter = function (inputFilter) {
        $(this).removeAttr('type');
        return this.on("input keydown keyup mousedown mouseup select contextmenu drop", function () {
            var max_value_condition;
            if ($(this).attr('max')) {
                max_value_condition = parseInt($(this).attr('max'));
            }
            var condition = max_value_condition ? /^\d*$/.test(this.value) && (this.value === "" || parseInt(this.value) <= max_value_condition) : /^\d*$/.test(this.value);
            if (condition) {
                this.oldValue = this.value;
                this.oldSelectionStart = this.selectionStart;
                this.oldSelectionEnd = this.selectionEnd;
            } else if (this.hasOwnProperty("oldValue")) {
                this.value = this.oldValue;
            }

        });
    };
}(jQuery));

$(document).ready(function () {
    var error_message = $(".error-message");

    var validateInput = (input, mess) => {
        $(input).html(mess);
    }

    validateInput(error_message, error_message.attr('mess'));

    $('#id_project').selectpicker({
        actionsBox: true,
        width: 'css-width',
        liveSearch: true,
    });
    $('#id_project').selectpicker('setStyle', 'btn-white border border rounded');
    $('#id_project').selectpicker('render');

    $('input.input-validation').change(function () {
        this.value = parseInt(this.value || 0);
    });
    $('input.input-validation').inputFilter();
})
