# Announcements — Odoo Module

Extension of the [`hr_reward_warning`](https://apps.odoo.com/apps/modules/hr_reward_warning) module, adding announcement templates, recurrence scheduling, popup (modal) notifications, and real-time delivery via the Odoo bus.

- **Author:** Bruno Bonassi Montico  
- **Version:** 19.0.0.0  
- **License:** AGPL-3  
- **Depends on:** `hr_reward_warning`

---

## Features

### Announcement Templates
Create reusable templates with rich HTML content and image attachments. When creating an announcement, simply select a template instead of writing the content from scratch every time.

### Recurrence Scheduling
Announcements can be sent automatically on a schedule via a daily cron job. Supported recurrence types:

| Type | Configuration |
|------|--------------|
| **None** | Sent once on approval |
| **Daily** | Every N days |
| **Weekly** | On selected weekdays |
| **Monthly** | On a specific day of the month |

The module automatically calculates the `next_send_date` and updates `last_send_date` after each sending.

### Popup (Modal) Notifications
Announcements can be configured to show as a popup modal to recipients. The modal is triggered in real time using Odoo's `bus.bus`, so users see it immediately upon login or while the session is active.

### Audience Targeting
Announcements can be sent to:
- All active users (company-wide)
- Specific employees
- Entire departments
- Employees by job position

### Preview
Managers can preview the announcement modal before approving it, using the **Preview** button on the announcement form.

---

## Usage

### Creating a Template
1. Go to **Announcements → Templates**.
2. Create a new template with a name, HTML body, and optional images.

### Creating an Announcement
1. Go to **Announcements → Announcements**.
2. Select a template, configure the recurrence, and define the target audience.
3. Enable **Popup** if you want the announcement to appear as a modal.
4. Use the **Preview** button to check how it will look before approving.
5. Approve the announcement — it will be sent immediately if within the active date range.

### Recurrence
- Set **Recurrence** to `Daily`, `Weekly`, or `Monthly`.
- The cron job runs once a day and automatically sends any approved announcements due today.

---

## Access Groups

| Group | Permissions |
|-------|-------------|
| **Announcement / User** | Read access to announcements and templates |
| **Announcement / Manager** | Full access, including create/edit/approve (inherits User) |

---

## Tests

The test suite (`tests/test_announcement_recurrence.py`) covers:
- Daily recurrence with custom intervals
- Weekly recurrence targeting a specific weekday
- Monthly recurrence with month-end edge cases (e.g., Feb 29)
- `_should_send_today` logic (send today vs. future date)
- Scheduled job triggering approved announcements
