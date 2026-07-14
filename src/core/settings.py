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
