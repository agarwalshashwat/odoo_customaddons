from odoo import api,fields,models,_
import logging
_logger = logging.getLogger(__name__)

class SchoolFeeWizard(models.TransientModel):
    _name = "school.fee.wizard"
    _description = "School Fee Wizard"

    student_id = fields.Many2one("school.student",string="Student ID")
    amount_paid = fields.Float(string="Amount Paid")
    total_fee = fields.Float(string="Total Fees")
    due_fee = fields.Float(compute = "DuesCalculator", string="Due Fees")

    @api.depends("total_fee","amount_paid")
    def DuesCalculator(self):
        for rec in self:
            rec.due_fee = 0
            if rec.total_fee and rec.amount_paid:
                rec.write({
                    "due_fee" : rec.total_fee - rec.amount_paid,
                })

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
                    "total_fee":self.total_fee,
                    "due_fee":self.due_fee,
                })
            # obj = self.env['school.fee.line'].create({
            #     "student_id": self.student_id,
            #     "due_fee": self.due_fee,
            #     "amount_paid": self.amount_paid,
            # })

        