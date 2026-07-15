import os
from gi.repository import Adw, Gio
from window import MarkdownViewerWindow

class MarkdownViewerApp(Adw.Application):
    def __init__(self):
        super().__init__(
            application_id="com.antiloop.MarkdownViewer",
            flags=Gio.ApplicationFlags.HANDLES_OPEN
        )

    def do_startup(self):
        Adw.Application.do_startup(self)

        action_quit = Gio.SimpleAction.new("quit", None)
        action_quit.connect("activate", self.on_quit_activated)
        self.add_action(action_quit)

        self.set_accels_for_action("app.quit", ["<Control>q"])
        self.set_accels_for_action("win.open", ["<Control>o"])
        self.set_accels_for_action("win.close_document", ["<Control>w"])
        self.set_accels_for_action("win.zoom_in", ["<Control>plus", "<Control>equal", "<Control>KP_Add"])
        self.set_accels_for_action("win.zoom_out", ["<Control>minus", "<Control>KP_Subtract"])
        self.set_accels_for_action("win.zoom_reset", ["<Control>0", "<Control>KP_0"])
        self.set_accels_for_action("win.find", ["<Control>f"])
        self.set_accels_for_action("win.print", ["<Control>p"])

    def do_activate(self):
        win = self.get_active_window()
        created = False
        if not win:
            win = MarkdownViewerWindow(application=self)
            created = True
        win.present()
        
        # Reopen the last viewed document if the app was started without arguments
        if created and not win.history.current_filepath:
            last_file = win.settings.last_opened_filepath
            if last_file and os.path.exists(last_file):
                win.open_file(last_file, save_to_history=True, is_explicit=False)

    def do_open(self, files, n_files, hint):
        win = self.get_active_window()
        if not win:
            win = MarkdownViewerWindow(application=self)
        win.present()
        if n_files > 0:
            # CLI launch is considered an explicit open action
            win.open_file(files[0].get_path(), save_to_history=True, is_explicit=True)

    def on_quit_activated(self, action, parameter):
        for window in list(self.get_windows()):
            window.close()
        self.quit()
