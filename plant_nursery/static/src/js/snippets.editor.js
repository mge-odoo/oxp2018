odoo.define('plant_nursery.snippets.editor', function (require) {
    'use strict';

    var sOptions = require('web_editor.snippets.options');

    sOptions.registry.sPromoPlant = sOptions.Class.extend({
        cleanForSave: function () {
            this.$target.find('.row').empty();
        },
        limit: function (previewMode, value) {
            // $target is our snippet
            this.$target.attr('data-limit', value);
            console.log(previewMode + 'coucou ' + value);
            this._render();
        },
        start: function () {
            return $.when(this._render(), this._super.apply(this, arguments));

        },
        _render: function () {
            // Restart the snippet
            this.trigger_up('animation_start_demand', {
                editableMode: true,
                $target: this.$target,
            });
        },
        // This method is also used to unset the option if not clickded
        _setActive: function () {
            this._super.apply(this, arguments);
            var self = this;
            this.$el.find('[data-limit]')
                .removeClass('active')
                .filter(function () {
                    var $elem = $(this);
                    var limit = $elem.data('limit');
                    return parseInt(self.$target.attr('data-limit')) === limit;
                })
                .addClass('active');
            }
    });
});
