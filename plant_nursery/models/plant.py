# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.addons.http_routing.models.ir_http import slug
from odoo.exceptions import UserError


class Category(models.Model):
    _name = 'nursery.plant.category'
    _description = 'Plant Category'
    _order = 'name'
    _inherit = ['mail.alias.mixin']

    name = fields.Char('Name', required=True)

    def get_alias_model_name(self, vals):
        return 'nursery.order'

    def get_alias_values(self):
        values = super(Category, self).get_alias_values()
        values['alias_defaults'] = {'category_id': self.id}
        return values


class Tag(models.Model):
    _name = 'nursery.plant.tag'
    _description = 'Plant Tag'
    _order = 'name'

    name = fields.Char('Name', required=True)
    color = fields.Integer('Color Index', default=10)


class Plants(models.Model):
    _name = 'nursery.plant'
    _description = 'Plant'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'website.seo.metadata', 'website.published.multi.mixin']

    name = fields.Char("Plant Name", required=True, track_visibility='always')
    price = fields.Float(track_visibility='onchange')
    description_short = fields.Html('Short description')
    description = fields.Html('Description')
    category_id = fields.Many2one('nursery.plant.category', string='Category')
    tag_ids = fields.Many2many('nursery.plant.tag', string='Tags')
    order_count = fields.Integer(compute='_compute_order_count',
                                 string="Total sold")
    number_in_stock = fields.Integer()
    image = fields.Binary("Plant Image", attachment=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible',
        index=True, required=True,
        default=lambda self: self.env.user)
    internal = fields.Boolean('Internal')
    promo = fields.Boolean('Is in Promotion')

    def _compute_order_count(self):
        for plant in self:
            plant.order_count = len(self.env['sale.order.line'].search([('plant_id', '=', plant.id)]))

    @api.constrains('number_in_stock')
    def _check_available_in_stock(self):
        for plant in self:
            if plant.number_in_stock < 0:
                raise UserError(_('Stock cannot be negative.'))

    def _compute_website_url(self):
        super(Plants, self)._compute_website_url()
        for plant in self:
            if plant.id:
                plant.website_url = '/plant/%s' % slug(plant)

    def _track_subtype(self, init_values):
        if 'price' in init_values:
            return 'plant_nursery.plant_price'
        return super(Plants, self)._track_subtype(init_values)

    def _track_template(self, tracking):
        res = super(Plants, self)._track_template(tracking)
        plant = self[0]
        changes, dummy = tracking[plant.id]
        if 'price' in changes:
            res['price'] = (self.env.ref('plant_nursery.mail_template_plant_price_updated'), {'composition_mode': 'comment'})
        return res
