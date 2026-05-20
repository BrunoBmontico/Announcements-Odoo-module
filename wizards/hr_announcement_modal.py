from odoo import fields, models

class HrAnnouncementModal(models.TransientModel):
    _name = "hr.announcement.modal"

    announcement_template_id = fields.Many2one(
        string="Announcement Template",
        comodel_name="hr.announcement.template",
        required=True
    )

    announcement = fields.Html(
        string="Template",
        related="announcement_template_id.template",
        help="Announcement message"
    )

    attachment_id = fields.Many2many(
        string="Images",
        comodel_name="ir.attachment",
        relation="doc_warning_rel",
        column1="doc_id",
        column2="attach_id4",
        related="announcement_template_id.attachment_id",
        readonly=False,
    )