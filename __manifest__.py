{
    "name":        "Announcements",
    "description": "Extension of hr_reward_warning.",
    "version":     "19.0.0.0",
    "license":     "AGPL-3",
    "author":      "Bruno Bonassi Montico",
    "depends":     ['hr_reward_warning'],

    "data": [
        "data/ir_cron.xml",
        "data/week_days.xml",

        "security/groups.xml",
        "security/ir.model.access.csv",

        "wizards/hr_announcement_modal.xml",

        "views/inherit_hr_announcement.xml",
        "views/hr_announcement_template.xml",
        "views/actions.xml",
        "views/menus.xml",
    ],
    
    'assets': {
        'web.assets_backend': [
            'ext_hr_reward_warning/static/src/js/image_carousel.js',
            'ext_hr_reward_warning/static/src/css/image_carousel.css',
            'ext_hr_reward_warning/static/src/js/announcement_listener.js',
        ],
    },
}