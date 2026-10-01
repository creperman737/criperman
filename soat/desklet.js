const Desklet = imports.ui.desklet;
const St = imports.gi.St;
const Mainloop = imports.mainloop;

function MyDesklet(metadata, desklet_id) {
    this._init(metadata, desklet_id);
}

MyDesklet.prototype = {
    __proto__: Desklet.Desklet.prototype,

    _init: function(metadata, desklet_id) {
        Desklet.Desklet.prototype._init.call(this, metadata, desklet_id);

        this.setHeader("CripOS Clock");

        this._box = new St.BoxLayout({
            vertical: true,
            style_class: "cripos-clock-container"
        });

        this._timeLabel = new St.Label({
            text: "00:00:00",
            style_class: "cripos-clock-time"
        });

        this._dateLabel = new St.Label({
            text: "",
            style_class: "cripos-clock-date"
        });

        this._box.add_actor(this._timeLabel);
        this._box.add_actor(this._dateLabel);
        this.setContent(this._box);
        this._updateClock();
    },

    _updateClock: function() {
        let now = new Date();
        let hours = String(now.getHours()).padStart(2, "0");
        let minutes = String(now.getMinutes()).padStart(2, "0");
        let seconds = String(now.getSeconds()).padStart(2, "0");

        this._timeLabel.set_text(hours + ":" + minutes + ":" + seconds);

        let days = [
            "Yakshanba", "Dushanba", "Seshanba", "Chorshanba",
            "Payshanba", "Juma", "Shanba"
        ];
        let day = String(now.getDate()).padStart(2, "0");
        let month = String(now.getMonth() + 1).padStart(2, "0");
        let year = now.getFullYear();
        this._dateLabel.set_text(
            days[now.getDay()] + ", " + day + "." + month + "." + year
        );
        this._timeout = Mainloop.timeout_add(1000, () => {
            this._updateClock();
            return false;
        });
    },

    on_desklet_removed: function() {
        if (this._timeout) {
            Mainloop.source_remove(this._timeout);
            this._timeout = null;
        }
    }
};

function main(metadata, desklet_id) {
    return new MyDesklet(metadata, desklet_id);
}
