from unittest.mock import patch
from datetime import date, timedelta
from odoo import fields
from odoo.tests.common import TransactionCase

class TestAnnouncementRecurrence(TransactionCase):

    def setUp(self):
        super().setUp()
        today = fields.Date.today()
        template = self.env["hr.announcement.template"].create({
            "name": "Test Template",
        })
        self.announcement = self.env["hr.announcement"].create({
            "announcement_reason": "Test",
            "announcement_template_id": template.id,
            "state": "approved",
            "date_start": today,
            "date_end": today + timedelta(days=365),
        })

    def test_daily_interval_2(self):
        self.announcement.recurrence_type = "daily"
        self.announcement.recurrence_interval = 2

        from_date = date(2024, 6, 10)
        result = self.announcement._compute_next_send_date(from_date=from_date)

        self.assertEqual(result, date(2024, 6, 12))

    def test_weekly_next_friday(self):
        friday = self.env.ref("vision_hr_reward_warning.week_day_friday")
        self.announcement.recurrence_type = "weekly"
        self.announcement.recurrence_interval = 1
        self.announcement.week_day_ids = [(6, 0, [friday.id])] 

        from_date = date(2024, 6, 10)
        result = self.announcement._compute_next_send_date(from_date=from_date)

        self.assertEqual(result, date(2024, 6, 14))

    def test_monthly_specific_day(self):
        self.announcement.recurrence_type = "monthly"
        self.announcement.recurrence_interval = 1
        self.announcement.month_day = date(2024, 1, 31) 

        from_date = date(2024, 1, 15)
        result = self.announcement._compute_next_send_date(from_date=from_date)

        self.assertEqual(result, date(2024, 2, 29))

    def test_should_send_when_next_date_is_today(self):
        self.announcement.recurrence_type = "daily"
        self.announcement.recurrence_interval = 1

        today = date.today()
        self.announcement.next_send_date = today

        self.assertTrue(self.announcement._should_send_today())

    def test_should_not_send_when_next_date_is_future(self):
        self.announcement.recurrence_type = "daily"
        self.announcement.recurrence_interval = 1
        self.announcement.next_send_date = date(2099, 1, 1)

        self.assertFalse(self.announcement._should_send_today())

    def test_run_scheduled_sends_approved_in_range(self):
        today = fields.Date.today()
        self.announcement.write({
            "recurrence_type": "daily",
            "recurrence_interval": 1,
            "next_send_date": today,
            "date_start": today,
            "date_end": today + timedelta(days=30),
        })

        with patch.object(
            type(self.announcement),
            'send_announcement',
            autospec=True
        ) as mock_send:
            self.env["hr.announcement"]._run_scheduled_announcements()
            mock_send.assert_called_once()