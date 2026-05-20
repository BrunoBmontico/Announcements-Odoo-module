from odoo import fields, models

class HrWeekDay(models.Model):
    _name = "hr.week.day"

    name = fields.Char(
        string="Nome"
    )

    code = fields.Selection(
        selection=[
            ("sunday", "Sunday"),
            ("monday", "Monday"),
            ("tuesday", "Tuesday"),
            ("wednesday", "Wednesday"),
            ("thursday", "Thursday"),
            ("friday", "Friday"),
            ("saturday", "Saturday"),
        ],
        string="Code"
    )