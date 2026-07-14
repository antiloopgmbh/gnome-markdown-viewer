import os
import json
from gi.repository import GLib

class AppSettings:
    def __init__(self):
        config_dir = os.path.join(GLib.get_user_config_dir(), "com.antiloop.MarkdownViewer")
        os.makedirs(config_dir, exist_ok=True)
        self.filepath = os.path.join(config_dir, "settings.json")
        self.data = {
            "show_left_sidebar": True,
            "show_right_sidebar": True
        }
        self.load()

    def load(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, 'r', encoding='utf-8') as f:
                    saved_data = json.load(f)
                    self.data.update(saved_data)
            except Exception as e:
                print("Failed to load settings:", e)

    def save(self):
        try:
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=4)
        except Exception as e:
            print("Failed to save settings:", e)

    @property
    def show_left_sidebar(self):
        return self.data.get("show_left_sidebar", True)

    @show_left_sidebar.setter
    def show_left_sidebar(self, value):
        self.data["show_left_sidebar"] = value
        self.save()

    @property
    def show_right_sidebar(self):
        return self.data.get("show_right_sidebar", True)

    @show_right_sidebar.setter
    def show_right_sidebar(self, value):
        self.data["show_right_sidebar"] = value
        self.save()

    @property
    def last_opened_filepath(self):
        return self.data.get("last_opened_filepath", None)

    @last_opened_filepath.setter
    def last_opened_filepath(self, value):
        self.data["last_opened_filepath"] = value
        self.save()

    @property
    def recent_files(self):
        return self.data.get("recent_files", [])

    def add_recent_file(self, filepath):
        filepath = os.path.abspath(filepath)
        recents = list(self.recent_files)
        if filepath in recents:
            recents.remove(filepath)
        recents.insert(0, filepath)
        self.data["recent_files"] = recents[:10]
        self.save()
