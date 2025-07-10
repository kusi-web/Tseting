from odoo import models, fields, api, _

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        result = super(StockPicking, self).button_validate()
        # Check if this picking is related to an RMA
        rma = self.env['custom.rma'].search([('picking_id', '=', self.id)], limit=1)
        if rma and self.state == 'done':
            current_stage = self.env.ref('custom_rma.stage_awaiting_stock')
            next_stage = self.env.ref('custom_rma.stage_awaiting_credit')
            if rma.stage_id.id == current_stage.id:
                rma.write({'stage_id': next_stage.id})
        return result
