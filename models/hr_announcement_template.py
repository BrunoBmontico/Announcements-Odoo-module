from odoo import fields, models

class HrAnnouncementTemplate(models.Model):
    _name = "hr.announcement.template"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(
        string="Name",
        required=True
    )

    template = fields.Html(
        string="Template"
    )

    attachment_id = fields.Many2many(
        string="Images",
        comodel_name="ir.attachment",
        relation="temp_img_rel",
    )