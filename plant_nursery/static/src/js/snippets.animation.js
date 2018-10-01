odoo.define('plant_nursery.snippets.animation', function (require) {
    "use strict";

    var core = require('web.core');
    var sAnimation = require('website.content.snippets.animation');

    sAnimation.registry.sPromoPlant = sAnimation.Class.extend({
        selector: ".s_promo_plants",
        xmlDependencies: ['/plant_nursery/static/src/xml/animation.xml'],

        init: function () {
            this._super.apply(this, arguments);
            this.plantsInPromo = [];
        },
        start: function () {
            return $.when(
                this._loadPlants(),
                this._super.apply(this, arguments)
            );
        },
        destroy: function () {
            // Remove the col before entering in edit mode
            this.$('.row').empty();
            this._super.apply(this, arguments);
        },
        _loadPlants: function () {
            if (this.editableMode) {
                this._renderPlants();
                return $.when();
            }
            var self = this;
            return this._rpc({
                model: 'nursery.plant',
                method: 'search_read',
                domain: [['promo', '=', true]],
                fields: ['name', 'description', 'image', 'price'],
                limit: this.$el.data('limit'),
            }).then(function (result) {
                self.plantsInPromo = result;
                self._renderPlants();
            });
        },
        _renderPlants: function () {
            if (this.editableMode) {
                var value = parseInt(this.$el.attr('data-limit'));
                this.$target.find('.row').empty();
                var $row = this.$target.find('.row');
                $row.empty();
                for (var i = 0; i < value; i++) {
                    $row.append($('<div>', {
                        class: 'col-md-3',
                        text: 'coucou',
                    }));
                }
            } else {
                this.$('.row').append(core.qweb.render('plant_nursery.promo_plants', {
                    widget: this,
                }));
            }

        },

    });
});
