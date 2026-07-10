#!/usr/bin/env /usr/bin/python3
import sys
from unittest.mock import MagicMock, patch

# Base mock widget to support general GtkWidget methods
class MockWidget:
    def set_vexpand(self, val): pass
    def set_hexpand(self, val): pass
    def set_size_request(self, w, h): pass
    def set_visible(self, val): self._visible = val
    def get_visible(self): return getattr(self, '_visible', True)
    def add_controller(self, controller): pass
    def add_action(self, action): pass

class MockGObject:
    class Object(MockWidget):
        def __init__(self, *args, **kwargs):
            pass

class MockGtk:
    Orientation = MagicMock()
    class PackType:
        START = 0
        END = 1
    class SelectionMode:
        NONE = 0
    class Box(MockWidget):
        def __init__(self, *args, **kwargs): pass
        def append(self, widget): pass
        def add_css_class(self, name): pass
    class Button(MockWidget):
        def __init__(self, *args, **kwargs): pass
        def connect(self, event, callback): pass
        def set_tooltip_text(self, text): pass
        def set_sensitive(self, state): pass
    class ToggleButton(Button):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self._active = False
        def set_active(self, active):
            self._active = active
        def get_active(self):
            return self._active
    class ScrolledWindow(MockWidget):
        def __init__(self, *args, **kwargs): pass
        def set_child(self, child): pass
    class ListBox(MockWidget):
        def __init__(self, *args, **kwargs):
            self.rows = []
        def connect(self, event, callback): pass
        def set_selection_mode(self, mode): pass
        def remove(self, row):
            if row in self.rows:
                self.rows.remove(row)
        def append(self, row):
            self.rows.append(row)
        def get_row_at_index(self, index):
            if index < len(self.rows):
                return self.rows[index]
            return None
        def select_row(self, row): pass
    class ListBoxRow(MockWidget):
        def __init__(self, *args, **kwargs): pass
        def set_child(self, child): pass
    class Label(MockWidget):
        def __init__(self, *args, **kwargs):
            self.label = kwargs.get('label', '')
        def set_margin_start(self, v): pass
        def set_margin_end(self, v): pass
        def set_margin_top(self, v): pass
        def set_margin_bottom(self, v): pass
        def set_markup(self, v): pass
        def set_text(self, v): pass
    class FileDialog:
        @classmethod
        def new(cls):
            fd = MagicMock()
            return fd
    class FileFilter:
        @classmethod
        def new(cls):
            ff = MagicMock()
            return ff
    class Paned(MockWidget):
        def __init__(self, *args, **kwargs): pass
        def set_start_child(self, child): pass
        def set_end_child(self, child): pass
        def set_resize_start_child(self, val): pass
        def set_resize_end_child(self, val): pass
        def set_shrink_start_child(self, val): pass
        def set_shrink_end_child(self, val): pass
        def set_position(self, val): pass
    class GestureClick(MockWidget):
        @classmethod
        def new(cls):
            g = MagicMock()
            g.get_current_button.return_value = 8
            return g
        def set_button(self, button): pass
        def connect(self, event, callback): pass
    class EventSequenceState:
        CLAIMED = 1

class MockAdw:
    class ApplicationWindow(MockGObject.Object):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
        def set_content(self, content): pass
        def set_default_size(self, w, h): pass
        def set_title(self, title): pass
    class HeaderBar(MockWidget):
        def __init__(self, *args, **kwargs): pass
        def pack_start(self, widget): pass
        def pack_end(self, widget): pass
    class OverlaySplitView(MockWidget):
        def __init__(self, *args, **kwargs):
            self._show_sidebar = False
        def set_sidebar_position(self, pos): pass
        def set_min_sidebar_width(self, w): pass
        def set_max_sidebar_width(self, w): pass
        def set_sidebar(self, sidebar): pass
        def set_content(self, content): pass
        def set_show_sidebar(self, show): self._show_sidebar = show
        def get_show_sidebar(self): return self._show_sidebar
    class StyleManager:
        def __init__(self):
            self.dark = False
        def get_dark(self):
            return self.dark
        def connect(self, event, callback): pass
        @classmethod
        def get_default(cls):
            if not hasattr(cls, '_instance'):
                cls._instance = MockAdw.StyleManager()
            return cls._instance
    class Application:
        def __init__(self, *args, **kwargs): pass
        def set_accels_for_action(self, action, accels): pass
        def add_action(self, action): pass
        def do_startup(self): pass

class MockWebKit:
    class WebView(MockWidget):
        def __init__(self, *args, **kwargs):
            self.load_html_calls = []
        def get_settings(self):
            s = MagicMock()
            return s
        def get_user_content_manager(self):
            m = MagicMock()
            return m
        def connect(self, event, callback): pass
        def load_html(self, html, base_uri):
            self.load_html_calls.append((html, base_uri))
    class PolicyDecisionType:
        NAVIGATION_ACTION = 1

class MockGio:
    AppInfo = MagicMock()
    ListStore = MagicMock()
    class SimpleAction:
        @classmethod
        def new(cls, name, parameter_type):
            s = MagicMock()
            return s
    class ApplicationFlags:
        HANDLES_OPEN = 1
    class File:
        @classmethod
        def new_for_path(cls, path):
            f = MagicMock()
            f.get_path.return_value = path
            return f

# Inject mocks into sys.modules
sys.modules['gi'] = MagicMock()
class MockGLib:
    @classmethod
    def set_prgname(cls, name): pass
    @classmethod
    def set_application_name(cls, name): pass

class MockGiRepository:
    Gtk = MockGtk
    Adw = MockAdw
    WebKit = MockWebKit
    Gio = MockGio
    GObject = MockGObject
    GLib = MockGLib

sys.modules['gi.repository'] = MockGiRepository

# Import the code to test (it will now use the mock classes)
from md_viewer import MarkdownViewerWindow
import unittest
import os
import tempfile

class TestMarkdownViewerPureLogic(unittest.TestCase):
    def setUp(self):
        self.window = MarkdownViewerWindow()

    def test_placeholder_rendering(self):
        self.window.show_placeholder()
        self.assertTrue(len(self.window.webview.load_html_calls) > 0)
        html, _ = self.window.webview.load_html_calls[-1]
        self.assertIn("No Markdown File Open", html)

    def test_navigation_history(self):
        with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as f1, \
             tempfile.NamedTemporaryFile(suffix=".md", delete=False) as f2:
            file1 = f1.name
            file2 = f2.name

        try:
            # Open file 1
            self.window.open_file(file1, save_to_history=True)
            self.assertEqual(self.window.current_filepath, os.path.abspath(file1))
            self.assertEqual(len(self.window.history_back), 0)

            # Open file 2
            self.window.open_file(file2, save_to_history=True)
            self.assertEqual(self.window.current_filepath, os.path.abspath(file2))
            self.assertEqual(len(self.window.history_back), 1)
            self.assertEqual(self.window.history_back[0], os.path.abspath(file1))

            # Go back
            self.window.go_back(None)
            self.assertEqual(self.window.current_filepath, os.path.abspath(file1))
            self.assertEqual(len(self.window.history_forward), 1)
            self.assertEqual(self.window.history_forward[0], os.path.abspath(file2))

            # Go forward
            self.window.go_forward(None)
            self.assertEqual(self.window.current_filepath, os.path.abspath(file2))
            self.assertEqual(len(self.window.history_back), 1)
        finally:
            os.remove(file1)
            os.remove(file2)

    def test_directory_loading(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            file_md1 = os.path.join(tmpdir, "a.md")
            file_md2 = os.path.join(tmpdir, "b.markdown")
            file_txt = os.path.join(tmpdir, "c.txt")

            with open(file_md1, "w") as f: f.write("# A")
            with open(file_md2, "w") as f: f.write("# B")
            with open(file_txt, "w") as f: f.write("# C")

            self.window.load_directory_files(file_md1)
            
            rows = self.window.file_list_box.rows
            self.assertEqual(len(rows), 2)
            filepaths = [r.filepath for r in rows]
            self.assertIn(os.path.abspath(file_md1), filepaths)
            self.assertIn(os.path.abspath(file_md2), filepaths)
            self.assertNotIn(os.path.abspath(file_txt), filepaths)

    def test_render_markdown_html_assembly(self):
        self.window.render_markdown("# Title", "/dummy/dir")
        self.assertTrue(len(self.window.webview.load_html_calls) > 0)
        html, _ = self.window.webview.load_html_calls[-1]
        self.assertIn("marked.min.js", html)
        self.assertIn("github-markdown.min.css", html)
        self.assertIn("highlight.min.js", html)
        self.assertIn("mermaid.min.js", html)

if __name__ == '__main__':
    unittest.main()
