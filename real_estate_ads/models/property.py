from odoo import  fields, models,api

class Property(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'


    name = fields.Char(string='Name',required=True)
    state = fields.Selection([
        ('new','New'),
        ('reserved','Offer Reserved'),
        ('accepted','Offer Accepted'),
        ('sold','Sold'),
        ('cancel','Cancelled')
    ],default='new',string='Status')
    tag_ids = fields.Many2many(comodel_name='estate.property.tag', string='Property Tag')
    type_id = fields.Many2one(comodel_name='estate.property.type', string='Property Type')
    description = fields.Char(string='Description')
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(string='Available From')
    expected_price = fields.Float(string='Expected Price')
    best_offer = fields.Float(string='Best Offer', compute= '_compute_best_price')
    selling_price = fields.Float(string='Selling Price',readonly=True)
    bedroom = fields.Integer(string='Bedroom')
    living_area = fields.Integer(string='Living Area(sqm)')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage', default=False)
    garden = fields.Boolean(string='Garden', default=False)
    garden_area = fields.Integer(string='Garden Area')
    garden_orientation = fields.Selection(
        [('north','North'),('south','South'),('east','East'),('west','West')],
        string='Garden Orientation', default='north', )
    offer_ids = fields.One2many('estate.property.offer','property_id',string='Offers')
    sales_id = fields.Many2one(comodel_name='res.users', string='Salesman')
    buyer_id = fields.Many2one(comodel_name='res.partner', string='Buyer',domain=[('is_company','=',True)] )
    phone= fields.Char(string='Phone', related='buyer_id.phone')

    @api.depends('living_area','garden_area')
    def _compute_total_area(self):
        for rec in self:
            rec.total_area = rec.living_area + rec.garden_area

    total_area = fields.Integer(string='Total Area' , compute=  _compute_total_area)

    def action_sold(self):
        self.state = 'sold'

    def action_cancel(self):
        self.state = 'cancel'


    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for rec in self:
            rec.offer_count = len(rec.offer_ids)

    offer_count=fields.Integer(string='Offer Count',compute= _compute_offer_count, store=True)

   #this code for intelligent button For offers 
    def action_property_view_offers(self):
        return {
            'type': 'ir.actions.act_window',
            'name': f"{self.name} - offers",
            'domain': [('property_id','=',self.id)],
            'view_mode': 'tree',
            'res_model': 'estate.property.view',
        }

    @api.depends('offer_ids')
    def _compute_best_price(self):
        for rec in self:
            if rec.offer_ids:
                rec.best_offer = max(rec.offer_ids.mapped('price'))
            else:
                rec.best_offer = 0






class PropertyType(models.Model):
    _name = 'estate.property.type'
    _description = ' Property Type'

    name = fields.Char(string='Name',required=True)
    description = fields.Char(string='Estate Property Type')

class PropertyTag(models.Model):
     _name = 'estate.property.tag'
     _description = 'Property Tag'

     name = fields.Char(string='Name', required=True)
     description = fields.Char(string='Estate Property Tag')
     color = fields.Integer(string='Color')