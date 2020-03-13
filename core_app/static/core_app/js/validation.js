class Validator {
    constructor () {
        const validateMsg = {
            DATE_FORMAT: 'Input field not in date format',
            URL_FORMAT: 'Input field not in url format',
            EMAIL_FORMAT: 'Input field not in email format',
            RANGE_DATE: 'From date must be lower or equal to To date'
        }
        this.validateMsg = validateMsg;
    }
    urlPattern = new RegExp(/^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$/gm);
    dateTimePattern = new RegExp('^(Jan|Feb|Mar|Apr|May|Jun|July|Aug|Nov|Oct|Dec|Sep)\\ [0-9]{1,2}\\,\\ [0-9]{1,4}$', 'i');
    emailPattern = new RegExp('', 'i');
    userNamePattern = new RegExp('', 'i');
    idPattern = new RegExp('', 'i');

    validateURL (url) {
        return !!this.urlPattern.test(url);
    }

    validateEmail (email) {
        return !!this.emailPattern.test(email);
    }

    validateDateTime (dateTimeInput) {
        return !!this.dateTimePattern.test(dateTimeInput);
    }

    validateDateFromTo (from, to) {
        const fromValue = new Date(from);
        const toValue = new Date(to);
        return fromValue <= toValue;
    }

    validateRequired (input) {

    }

    validateLimitLength (input) {

    }

    validateUsername (username) {

    }

    validateId (id) {

    }

    validateOnlyNumber (input) {

    }
}

export default Validator;