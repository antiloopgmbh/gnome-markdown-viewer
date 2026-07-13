import os
from gi.repository import Gtk, GObject, Pango, GLib

class FileSidebar(Gtk.Box):
    __gsignals__ = {
        'file-activated': (GObject.SignalFlags.RUN_FIRST, None, (str,))
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

        # Folder Icon
        icon = Gtk.Image.new_from_icon_name("folder-symbolic")
        header_box.append(icon)

        # Folder Name Label
        self.title_label = Gtk.Label(xalign=0.0)
        self.title_label.set_hexpand(True)
        self.title_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.title_label.set_markup("<b>Folder</b>")
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
        self.list_box.connect("row-activated", self.on_row_activated)
        scroll.set_child(self.list_box)

    def on_row_activated(self, list_box, row):
        if row and hasattr(row, 'filepath'):
            self.emit('file-activated', row.filepath)

    def load_directory(self, current_filepath):
        # Clear previous list
        while True:
            row = self.list_box.get_row_at_index(0)
            if not row:
                break
            self.list_box.remove(row)

        dir_path = os.path.dirname(os.path.abspath(current_filepath))
        folder_name = os.path.basename(dir_path)
        
        # Set dynamic folder title and full path tooltip
        escaped_folder_name = GLib.markup_escape_text(folder_name)
        self.title_label.set_markup(f"<b>{escaped_folder_name}</b>")
        self.title_label.set_tooltip_text(dir_path)

        try:
            files = [f for f in os.listdir(dir_path) if f.lower().endswith(('.md', '.markdown'))]
            files.sort(key=str.lower)
            for f in files:
                full_path = os.path.join(dir_path, f)
                label = Gtk.Label(label=f, xalign=0.0)
                label.set_margin_start(12)
                label.set_margin_end(12)
                label.set_margin_top(8)
                label.set_margin_bottom(8)

                row = Gtk.ListBoxRow()
                row.set_child(label)
                row.filepath = full_path

                self.list_box.append(row)

                if os.path.abspath(full_path) == os.path.abspath(current_filepath):
                    self.list_box.select_row(row)
        except Exception as e:
            print(f"Error loading directory: {e}")
