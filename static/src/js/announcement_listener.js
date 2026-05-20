/** @odoo-module **/

import { registry } from "@web/core/registry";
import { user } from "@web/core/user";

const announcementListenerService = {
    dependencies: ["bus_service", "action"],

    start(env, { bus_service, action }) {
        const channel = `res.partner/${user.partnerId}`;

        bus_service.addChannel(channel);

        bus_service.subscribe("open_announcement_modal", (payload) => {
            action.doAction(payload);
        });
    }
};

registry.category("services").add("announcement_listener_service", announcementListenerService);