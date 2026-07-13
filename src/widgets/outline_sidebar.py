import os
import json
from gi.repository import Gtk, GObject, Pango, GLib

class OutlineSidebar(Gtk.Box):
    __gsignals__ = {
        'heading-activated': (GObject.SignalFlags.RUN_FIRST, None, (str,))
    }

    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        self.set_size_request(240, -1)

        # Header Box
        header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        header_box.set_margin_start(12)
        header_box.set_margin_end(12)
        header_box.set_margin_top(12)
        header_box.set_margin_bottom(8)

        # Document Icon
        icon = Gtk.Image.new_from_icon_name("text-x-generic-symbolic")
        header_box.append(icon)

        # File Name Label
        self.title_label = Gtk.Label(xalign=0.0)
        self.title_label.set_hexpand(True)
        self.title_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.title_label.set_markup("<b>Document</b>")
        header_box.append(self.title_label)

        self.append(header_box)

        # Separator Line
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        self.append(separator)

        # ScrolledWindow for ListBox
        scroll = Gtk.ScrolledWindow()
        scroll.set_vexpand(True)
        self.append(scroll)

        self.list_box = Gtk.ListBox()
        self.list_box.set_selection_mode(Gtk.SelectionMode.NONE)
        self.list_box.connect("row-activated", self.on_row_activated)
        scroll.set_child(self.list_box)

    def on_row_activated(self, list_box, row):
        if row and hasattr(row, 'heading_id'):
            self.emit('heading-activated', row.heading_id)

    def set_filename(self, filepath):
        filename = os.path.basename(filepath)
        escaped_filename = GLib.markup_escape_text(filename)
        self.title_label.set_markup(f"<b>{escaped_filename}</b>")
        self.title_label.set_tooltip_text(filepath)

    def populate(self, outline_json_str):
        # Clear outline
        while True:
            row = self.list_box.get_row_at_index(0)
            if not row:
                break
            self.list_box.remove(row)

        try:
            outline = json.loads(outline_json_str)
            for item in outline:
                level = item.get('level', 1)
                text = item.get('text', '')
                heading_id = item.get('id', '')

                label = Gtk.Label(label=text, xalign=0.0)
                indent = (level - 1) * 12
                label.set_margin_start(12 + indent)
                label.set_margin_end(12)
                label.set_margin_top(4)
                label.set_margin_bottom(4)

                if level == 1:
                    escaped_text = GLib.markup_escape_text(text)
                    label.set_markup(f"<b>{escaped_text}</b>")
                else:
                    label.set_text(text)

                row = Gtk.ListBoxRow()
                row.set_child(label)
                row.heading_id = heading_id
                self.list_box.append(row)
        except Exception as e:
            print(f"Error parsing outline in widget: {e}")
