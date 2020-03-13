import Validator from './validation.js';

const validator = new Validator();

function onChangeDateTime(event) {
    const target = $(this).is('input') ? $(this) : $(this).find('input');
    const card = $(this).closest('.card');
    const container = target.parent();
    let dateValue = target.val();
    let propsCondition = null;
    let valueCondition = null;
    let subblingContainer = null;
    if (!validator.validateDateTime(dateValue)) {
        this.setCustomValidity(validator.validateMsg.DATE_FORMAT)
        return;
    }
    switch (target.attr('name')) {
        case 'from_date':
            valueCondition = card.find('input[name*="to_date"]').val();
            subblingContainer = card.find('input[name*="to_date"]').parent();
            propsCondition = 'minDate';
            if (!validator.validateDateFromTo(dateValue, valueCondition)) {
                this.setCustomValidity(validator.validateMsg.RANGE_DATE)
                return;
            }
            break;
        case 'to_date':
            valueCondition = card.find('input[name*="from_date"]').val();
            subblingContainer = card.find('input[name*="from_date"]').parent();
            propsCondition = 'maxDate';
            if (!validator.validateDateFromTo(valueCondition, dateValue)) {
                this.setCustomValidity(validator.validateMsg.RANGE_DATE)
                return;
            }
            break;
    }
    this.setCustomValidity('');
    subblingContainer.datetimepicker(propsCondition, new Date(dateValue));
}

$(document).ready(function () {
    $('.datetime-picker').datetimepicker({
        format: 'MMM DD, YYYY',
    });

    $('li.active').removeClass('active');
    $('a[href="' + location.pathname + '"]').closest('li').addClass('active');

    Date.prototype.addDays = function (days) {
        var dat = new Date(this.valueOf())
        dat.setDate(dat.getDate() + days);
        return dat;
    }

    $('.datetime-picker').on('change.datetimepicker', function () {
        const dateInput = $(this).find('input');
        dateInput.keyup();
    });

    $('.datetime-picker input').on('keyup', onChangeDateTime);
    $('.datetime-picker input').keyup();
});