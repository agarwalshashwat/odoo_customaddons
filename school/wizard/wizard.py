from odoo import api,fields,models,_
import logging
_logger = logging.getLogger(__name__)

class SchoolFeeWizard(models.TransientModel):
    _name = "school.fee.wizard"
    _description = "School Fee Wizard"

    student_id = fields.Many2one("school.student",string="Student ID")
    amount_paid = fields.Float(string="Amount Paid")

    def action_payment_register(self):
        self.ensure_one()
        active_model = self.env.context.get("active_model", False)
        active_id = self.env.context.get("active_id", 0)
        if active_model == "school.fee" and active_id:
            active_obj = self.env["school.fee"].browse(active_id)
            if active_obj:
                active_obj.write({
                    "student_id" : self.student_id,
                    "amount_paid": self.amount_paid,
                })