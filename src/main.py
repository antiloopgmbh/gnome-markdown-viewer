#!/usr/bin/env python3
import sys
import os
import gi

# Ensure GTK4 and Libadwaita are loaded
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
gi.require_version('WebKit', '6.0')

from gi.repository import GLib

# Add current folder to sys.path to allow relative core and widgets imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import MarkdownViewerApp

if __name__ == "__main__":
    GLib.set_prgname("com.antiloop.MarkdownViewer")
    GLib.set_application_name("Antiloop Markdown Viewer")
    app = MarkdownViewerApp()
    try:
        sys.exit(app.run(sys.argv))
    except KeyboardInterrupt:
        sys.exit(0)
