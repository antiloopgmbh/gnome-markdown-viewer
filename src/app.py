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
        action_quit.connect("activate", lambda a, p: self.quit())
        self.add_action(action_quit)

        self.set_accels_for_action("app.quit", ["<Control>q"])
        self.set_accels_for_action("win.open", ["<Control>o"])
        self.set_accels_for_action("win.close", ["<Control>w"])

    def do_activate(self):
        win = self.get_active_window()
        if not win:
            win = MarkdownViewerWindow(application=self)
        win.present()

    def do_open(self, files, n_files, hint):
        win = self.get_active_window()
        if not win:
            win = MarkdownViewerWindow(application=self)
        win.present()
        if n_files > 0:
            win.open_file(files[0].get_path(), save_to_history=True)
