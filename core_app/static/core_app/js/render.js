
class Renderer {
    
    constructor() {
        const spinner = $(` <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true">
                            </span>
                            <span class="sr-only">
                                Loading...
                            </span>`);
        
    }

    toggleLoadBtn (elm, value) {
        elm.empty();
        if (elm.hasAttr('disabled')) {
            elm.append(value);
            elm.removeAttr('disabled');
        } else {
            elm.append(this.spinner);
            elm.attr('disabled', true);
        }
    }

    showValidation (elm, msg) {
        elm.setCustomValidity(msg);
    }

    showErrMsg (container, msg) {
        const errContainer = $(`<div class="error-msg p-3 mb-2 text-danger">${msg}</div>`);
        container.append(errContainer);
    }

    removeErrors () {
        $('body').remove('.error-msg');
    }

    removeChilds (container, childs) {
        if (typeof(childs) !== 'undefined' && Array.isArray(childs)) {
            for (let i = 0; i < childs.length; i++) {
                container.find(childs[i]).remove();
            }
        } else {
            container.find(childs).remove();
        }
    }

    addChilds (container, childs) {
        if (typeof(childs) !== 'undefined' && Array.isArray(childs)) {
            for (let i = 0; i < childs.length; i++) {
                container.append(childs[i]);
            }
        } else {
            container.append(childs);
        }
    }
    
    toggleValidate (elm, valid, msg) {

    }
}

export default Renderer;