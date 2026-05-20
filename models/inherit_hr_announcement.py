from odoo import fields, models
from dateutil.relativedelta import relativedelta
from datetime import timedelta
import calendar

class InheritHrAnnouncement(models.Model):
    _inherit = "hr.announcement"
    _rec_name = "announcement_reason"

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

    modal = fields.Boolean(
        string="Popup"
    )

    recurrence_type = fields.Selection(
        string="Recurrence",
        selection=[
            ("none","None"),
            ("daily","Daily"),
            ("weekly","Weekly"),
            ("monthly","Monthly"),
        ],
        default="none"
    )

    recurrence_interval = fields.Integer(
        string="Interval",
        default=1,
        help="Sending interval (e.g., every two days)"
    )

    week_day_ids = fields.Many2many(
        string="Week Day",
        comodel_name="hr.week.day",
        relation="hr_announcement_week_day_rel",
        column1="announcement_id",
        column2="week_day_id",
    )

    month_day = fields.Date(
        string="Month Day"
    )

    next_send_date = fields.Date(
        string="Next Send",
        readonly=True
    )

    last_send_date = fields.Date(
        string="Last Send",
        readonly=True
    )

    def action_hr_announcement_preview(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Announcement",
            "res_model": "hr.announcement.modal",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_announcement_template_id": self.announcement_template_id.id,
            },
        }

    def _compute_next_send_date(self, from_date=None):
        if self.recurrence_type == "none":
            return False
        else:
            date = from_date or fields.Date.today()

            if self.recurrence_type == "daily":
                return date + timedelta(days=self.recurrence_interval)
            elif self.recurrence_type == "weekly":
                WEEK_DAY_MAP = {
                    "monday": 0, 
                    "tuesday": 1, 
                    "wednesday": 2,
                    "thursday": 3, 
                    "friday": 4,
                    "saturday": 5, 
                    "sunday": 6,
                }
                selected_codes = self.week_day_ids.mapped("code")
                if selected_codes:
                    next_date = None
                    for i in range(1, 8):
                        candidate = date + timedelta(days=i)
                        candidate_code = list(WEEK_DAY_MAP.keys())[candidate.weekday()]
                        if candidate_code in selected_codes:
                            next_date = candidate
                            break
                    return next_date
                else:
                    return date + timedelta(weeks=self.recurrence_interval)
            elif self.recurrence_type == "monthly":
                next_month = date + relativedelta(months=self.recurrence_interval)

                if self.month_day:
                    target_day = self.month_day.day

                    last_day = calendar.monthrange(next_month.year, next_month.month)[1]
                    target_day = min(target_day, last_day)
                    return next_month.replace(day=target_day)
                
                return next_month
            
    def _should_send_today(self):
        if self.recurrence_type == "none":
            return False
        else:
            today = fields.Date.today()
            if not self.next_send_date:
                return True
            else:
                return self.next_send_date <= today
            
    def _do_recurrent_send(self):
        today = fields.Date.today()

        self.send_announcement()

        next_date = self._compute_next_send_date(from_date=today)
        self.write({
            "last_send_date": today,
            "next_send_date": next_date,
        })

    def _run_scheduled_announcements(self):
        today = fields.Date.today()
        announcements = self.search([
            ("state", "=", "approved"),
            ("recurrence_type", "!=", "none"),
            ("date_start", "<=", today),
            ("date_end", ">=", today),
        ])
        for announcement in announcements:
            if announcement._should_send_today():
                announcement._do_recurrent_send()

    def _get_employee(self, partner_ids):
        partner_ids += self.employee_ids.filtered("user_id").mapped("user_id.partner_id.id")

    def _get_department(self, partner_ids):
        employees = self.department_ids.mapped("member_ids")
        partner_ids += employees.filtered("user_id").mapped("user_id.partner_id.id")
    
    def _get_job_position(self, partner_ids):
        employees = self.env["hr.employee"].search([("job_id", "in", self.position_ids.ids)])
        partner_ids += employees.filtered("user_id").mapped("user_id.partner_id.id")

    def _send_announcement_bus(self, partner_ids):
        payload = {
            "type": "ir.actions.act_window",
            "res_model": "hr.announcement.modal",
            "view_mode": "form",
            "target": "new",
            "views": [[False, "form"]],
            "context": {
                "default_announcement_template_id": self.announcement_template_id.id,
            }
        }

        for partner_id in partner_ids:
            channel = f"res.partner/{partner_id}"
            self.env["bus.bus"]._sendone(channel, "open_announcement_modal", payload)

    def _is_within_date_range(self):
        today = fields.Date.today()
        return self.date_start <= today <= self.date_end

    def send_announcement(self):
        template = self.announcement_template_id.template or self.announcement_reason
        partner_ids = []

        if self.is_announcement:
            users = self.env["res.users"].search([("active", "=", True)])
            partner_ids = users.mapped("partner_id.id")
        else:
            if self.announcement_type == "employee":
                self._get_employee(partner_ids)
            elif self.announcement_type == "department":
                self._get_department(partner_ids)
            elif self.announcement_type == "job_position":
                self._get_job_position(partner_ids)

        self.message_post(
            body=template,
            message_type="notification",
            subtype_xmlid="mail.mt_comment",
            partner_ids=partner_ids,
        )

        if self.modal:
            self._send_announcement_bus(partner_ids)

    def write(self, vals):
        record = super().write(vals)

        if vals.get("state") == "approved":
            for record in self:
                if record._is_within_date_range():
                    record.send_announcement()

                if record.recurrence_type != "none":
                    record.next_send_date = record._compute_next_send_date()
        return record