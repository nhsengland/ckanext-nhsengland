this.ckan.module('confirm-dataset-update', function (jQuery, _) {
    return {
    /* An object of module options */
	options: {
      /* Locale options can be overidden with data-module-i18n attribute */
	    i18n: {
		heading: _('Confirm Update'),
		content: _('Are you sure you want to update this dataset ? It is now publically viewable!'),
		confirm: _('Update'),
		cancel: _('Cancel')
	    },
	    template: [
		'<div class="modal">',
		'<div class="modal-header">',
		'<button type="button" class="close" data-dismiss="modal">x</button>',
		'<h3></h3>',
		'</div>',
		'<div class="modal-body"></div>',
		'<div class="modal-footer">',
		'<button class="btn btn-cancel"></button>',
		'<button class="btn btn-primary"></button>',
		'</div>',
        '</div>'
	    ].join('\n')
	},

    /* Sets up the event listeners for the object. Called internally by
     * module.createInstance().
     *
     * Returns nothing.
     */
	initialize: function () {
	    jQuery.proxyAll(this, /_on/);
	    this.el.on('click', this._onClick);
	    this.private = this.el.attr('data-private') == 'True';
	},

    /* Presents the user with a confirm dialogue to ensure that they wish to
     * continue with the current action.
     *
     * Examples
     *
     *   jQuery('.delete').click(function () {
     *     module.confirm();
     *   });
     *
     * Returns nothing.
     */
	confirm: function () {
	    this.sandbox.body.append(this.createModal());
	    this.modal.modal('show');
	    
	    // Center the modal in the middle of the screen.
	    this.modal.css({
		'margin-top': this.modal.height() * -0.5,
		'top': '50%'
	    });
	},

    /* Performs the action for the current item.
     *
     * Returns nothing.
     */
	performAction: function () {
	    this.private = ! this.private;
	    this.el.click();
	},

    /* Creates the modal dialog, attaches event listeners and localised
     * strings.
     *
     * Returns the newly created element.
     */
	createModal: function () {
	    if (!this.modal) {
		var element = this.modal = jQuery(this.options.template);
		element.on('click', '.btn-primary', this._onConfirmSuccess);
		element.on('click', '.btn-cancel', this._onConfirmCancel);
		element.modal({show: false});

		element.find('h3').text(this.i18n('heading'));
		element.find('.modal-body').text(this.i18n('content'));
		element.find('.btn-primary').text(this.i18n('confirm'));
		element.find('.btn-cancel').text(this.i18n('cancel'));
	    }
	    return this.modal;
	},

    /* Event handler that displays the confirm dialog */
	_onClick: function (event) {
	    var privatep = $('#field-private').val() == "True";
	    if(!privatep && this.private){
		event.preventDefault();
		this.confirm();		
	    }
	},

    /* Event handler for the success event */
	_onConfirmSuccess: function (event) {
	    this.performAction();
	},

    /* Event handler for the cancel event */
	_onConfirmCancel: function (event) {
	    this.modal.modal('hide');
	}
    };
});
