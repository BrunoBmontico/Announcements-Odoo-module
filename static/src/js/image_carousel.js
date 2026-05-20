/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Component, useState, xml } from "@odoo/owl";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

class ImageCarouselField extends Component {
    static props = { ...standardFieldProps };
    static template = xml`
        <div class="o_image_carousel">
            <div class="carousel-wrapper">
                <button class="fa fa-chevron-left carousel-btn" t-on-click="prev"/>
                <div class="carousel-image-box">
                    <img 
                        t-att-src="currentImageUrl"
                        class="carousel-img"
                    />
                    <div class="carousel-counter">
                        <t t-esc="state.current + 1"/> / <t t-esc="attachments.length"/>
                    </div>
                </div>
                <button class="fa fa-chevron-right carousel-btn" t-on-click="next"/>
            </div>
        </div>
    `;

    setup() {
        this.state = useState({ current: 0 });
    }

    get attachments() {
        const value = this.props.record.data[this.props.name];
        if (!value) return [];
        return value.currentIds;
    }

    get currentImageUrl() {
        const ids = this.attachments;
        if (!ids.length) return "";
        const attachment_id = ids[this.state.current];
        return `/web/image/ir.attachment/${attachment_id}/datas`;
    }

    prev() {
        const len = this.attachments.length;
        this.state.current = (this.state.current - 1 + len) % len;
    }

    next() {
        this.state.current = (this.state.current + 1) % this.attachments.length;
    }
}

registry.category("fields").add("image_carousel", {
    component: ImageCarouselField,
    supportedTypes: ["many2many"],
});