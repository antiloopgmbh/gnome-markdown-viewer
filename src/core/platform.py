from abc import ABC, abstractmethod
import gi
from gi.repository import Gtk, Gio

try:
    gi.require_version('Granite', '7.0')
    from gi.repository import Granite
    HAS_GRANITE = True
except (ImportError, ValueError):
    HAS_GRANITE = False

HAS_ADW = False
try:
    gi.require_version('Adw', '1')
    from gi.repository import Adw
    HAS_ADW = True
except (ImportError, ValueError):
    pass


class PlatformStrategy(ABC):
    @abstractmethod
    def get_base_app_class(self):
        pass

    @abstractmethod
    def get_base_window_class(self):
        pass

    @abstractmethod
    def init_app(self, app):
        pass

    @abstractmethod
    def create_header_bar(self):
        pass

    @abstractmethod
    def setup_window_layout(self, window, main_box, header_bar):
        pass

    @abstractmethod
    def init_theme_monitoring(self, window, callback):
        pass

    @abstractmethod
    def is_dark_mode(self, window):
        pass


class ElementaryPlatformStrategy(PlatformStrategy):
    def get_base_app_class(self):
        return Gtk.Application

    def get_base_window_class(self):
        return Gtk.ApplicationWindow

    def init_app(self, app):
        Granite.init()

    def create_header_bar(self):
        return Gtk.HeaderBar()

    def setup_window_layout(self, window, main_box, header_bar):
        window.set_child(main_box)
        window.set_titlebar(header_bar)

    def init_theme_monitoring(self, window, callback):
        window.granite_settings = Granite.Settings.get_default()
        window.granite_settings.connect("notify::prefers-color-scheme", callback)

    def is_dark_mode(self, window):
        try:
            return window.granite_settings.prefers_color_scheme == Granite.Settings.ColorScheme.DARK
        except Exception:
            return False


class GnomePlatformStrategy(PlatformStrategy):
    def get_base_app_class(self):
        if HAS_ADW:
            return Adw.Application
        return Gtk.Application

    def get_base_window_class(self):
        if HAS_ADW:
            return Adw.ApplicationWindow
        return Gtk.ApplicationWindow

    def init_app(self, app):
        pass

    def create_header_bar(self):
        if HAS_ADW:
            return Adw.HeaderBar()
        return Gtk.HeaderBar()

    def setup_window_layout(self, window, main_box, header_bar):
        if HAS_ADW:
            window.set_content(main_box)
            main_box.append(header_bar)
        else:
            window.set_child(main_box)
            window.set_titlebar(header_bar)

    def init_theme_monitoring(self, window, callback):
        if HAS_ADW:
            window.style_manager = Adw.StyleManager.get_default()
            if window.style_manager:
                window.style_manager.connect("notify::dark", callback)
        else:
            window.style_manager = None

    def is_dark_mode(self, window):
        if HAS_ADW and window.style_manager:
            return window.style_manager.get_dark()
        return False


if HAS_GRANITE:
    current_platform = ElementaryPlatformStrategy()
else:
    current_platform = GnomePlatformStrategy()
