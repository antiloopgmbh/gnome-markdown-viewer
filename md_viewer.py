#!/usr/bin/env /usr/bin/python3
import sys
import os
import json
import urllib.parse
import gi

# Ensure GTK4 and Libadwaita are loaded
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
gi.require_version('WebKit', '6.0')

from gi.repository import Gtk, Adw, WebKit, Gio, GObject, GLib

class MarkdownViewerWindow(Adw.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_default_size(1000, 700)
        self.set_title("Antiloop Markdown Viewer")

        self.current_filepath = None
        self.history_back = []
        self.history_forward = []

        # Setup main container
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_content(self.main_box)

        # Header Bar
        self.header_bar = Adw.HeaderBar()
        self.main_box.append(self.header_bar)

        # Toggle Left Sidebar Button (File browser)
        self.btn_left_sidebar = Gtk.ToggleButton(icon_name="folder-symbolic")
        self.btn_left_sidebar.set_tooltip_text("Toggle file sidebar")
        self.btn_left_sidebar.connect("toggled", self.toggle_left_sidebar)
        self.header_bar.pack_start(self.btn_left_sidebar)

        # Open Button
        self.btn_open = Gtk.Button(icon_name="document-open-symbolic")
        self.btn_open.set_tooltip_text("Open markdown file")
        self.btn_open.connect("clicked", lambda x: self.show_file_chooser())
        self.header_bar.pack_start(self.btn_open)

        # Navigation box (Back / Forward)
        self.nav_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.nav_box.add_css_class("linked")
        self.btn_back = Gtk.Button(icon_name="go-previous-symbolic")
        self.btn_back.set_tooltip_text("Go back")
        self.btn_back.set_sensitive(False)
        self.btn_back.connect("clicked", self.go_back)
        self.btn_forward = Gtk.Button(icon_name="go-next-symbolic")
        self.btn_forward.set_tooltip_text("Go forward")
        self.btn_forward.set_sensitive(False)
        self.btn_forward.connect("clicked", self.go_forward)
        self.nav_box.append(self.btn_back)
        self.nav_box.append(self.btn_forward)
        self.header_bar.pack_start(self.nav_box)

        # Toggle Right Sidebar Button (Outline)
        self.btn_right_sidebar = Gtk.ToggleButton(icon_name="view-list-symbolic")
        self.btn_right_sidebar.set_tooltip_text("Toggle outline sidebar")
        self.btn_right_sidebar.connect("toggled", self.toggle_right_sidebar)
        self.header_bar.pack_end(self.btn_right_sidebar)

        # Outer Paned (Left Sidebar + Inner Area)
        self.left_paned = Gtk.Paned(orientation=Gtk.Orientation.HORIZONTAL)
        self.left_paned.set_vexpand(True)
        self.left_paned.set_hexpand(True)
        self.left_paned.set_position(240)
        self.left_paned.set_resize_start_child(False)
        self.left_paned.set_shrink_start_child(False)
        self.left_paned.set_resize_end_child(True)
        self.main_box.append(self.left_paned)

        # Left Sidebar Content (File Browser)
        self.file_list_scroll = Gtk.ScrolledWindow()
        self.file_list_scroll.set_size_request(240, -1)
        self.file_list_box = Gtk.ListBox()
        self.file_list_box.connect("row-activated", self.on_file_row_activated)
        self.file_list_scroll.set_child(self.file_list_box)
        self.left_paned.set_start_child(self.file_list_scroll)

        # Inner Paned (Main Content + Right Sidebar)
        self.right_paned = Gtk.Paned(orientation=Gtk.Orientation.HORIZONTAL)
        self.right_paned.set_vexpand(True)
        self.right_paned.set_hexpand(True)
        self.right_paned.set_position(520) # 1000 - 240 (left sidebar) - 240 (right sidebar) = 520 for webview
        self.right_paned.set_resize_start_child(True)
        self.right_paned.set_resize_end_child(False)
        self.right_paned.set_shrink_end_child(False)
        self.left_paned.set_end_child(self.right_paned)

        # Main Content: WebKit WebView
        self.webview = WebKit.WebView()
        self.webview.set_vexpand(True)
        self.webview.set_hexpand(True)
        self.right_paned.set_start_child(self.webview)

        # Right Sidebar Content (Outline)
        self.outline_scroll = Gtk.ScrolledWindow()
        self.outline_scroll.set_size_request(240, -1)
        self.outline_list_box = Gtk.ListBox()
        self.outline_list_box.set_selection_mode(Gtk.SelectionMode.NONE)
        self.outline_list_box.connect("row-activated", self.on_outline_row_activated)
        self.outline_scroll.set_child(self.outline_list_box)
        self.right_paned.set_end_child(self.outline_scroll)

        # Configure WebKit Settings
        settings = self.webview.get_settings()
        settings.set_allow_file_access_from_file_urls(True)
        settings.set_allow_universal_access_from_file_urls(True)
        settings.set_enable_developer_extras(True)

        # WebKit Script Message Handler for outline
        manager = self.webview.get_user_content_manager()
        manager.register_script_message_handler("outline")
        manager.connect("script-message-received::outline", self.on_outline_received)

        # WebKit Navigation Intercept
        self.webview.connect("decide-policy", self.on_decide_policy)

        # Mouse gestures for back/forward side buttons (Button 8 and 9)
        self.mouse_gesture = Gtk.GestureClick.new()
        self.mouse_gesture.set_button(0) # Listen to all buttons
        self.mouse_gesture.connect("pressed", self.on_mouse_button_pressed)
        self.webview.add_controller(self.mouse_gesture)

        # Dark mode listener
        self.style_manager = Adw.StyleManager.get_default()
        self.style_manager.connect("notify::dark", self.on_theme_changed)

        # Show placeholder
        self.show_placeholder()

    def show_placeholder(self):
        is_dark = self.style_manager.get_dark()
        bg_color = "#1e1e1e" if is_dark else "#fafafa"
        fg_color = "#aaaaaa" if is_dark else "#666666"
        placeholder_html = f"""<html><body style='font-family:sans-serif; text-align:center; padding-top:100px; color:{fg_color}; background-color:{bg_color};'>
            <h2 style='margin-bottom:8px;'>No Markdown File Open</h2>
            <p style='margin-top:0;'>Select a file using the Open button.</p>
        </body></html>"""
        self.webview.load_html(placeholder_html, None)
        self.file_list_scroll.set_visible(False)
        self.outline_scroll.set_visible(False)
        self.btn_left_sidebar.set_active(False)
        self.btn_right_sidebar.set_active(False)
        self.btn_left_sidebar.set_sensitive(False)
        self.btn_right_sidebar.set_sensitive(False)

    def open_file(self, filepath, save_to_history=True):
        filepath = os.path.abspath(filepath)
        if not os.path.exists(filepath):
            return

        if save_to_history and self.current_filepath:
            self.history_back.append(self.current_filepath)
            self.history_forward.clear()
            self.btn_back.set_sensitive(True)
            self.btn_forward.set_sensitive(False)

        self.current_filepath = filepath
        self.set_title(f"{os.path.basename(filepath)} - Antiloop Markdown Viewer")

        self.btn_left_sidebar.set_sensitive(True)
        self.btn_right_sidebar.set_sensitive(True)
        self.btn_left_sidebar.set_active(True)
        self.btn_right_sidebar.set_active(True)
        self.file_list_scroll.set_visible(True)
        self.outline_scroll.set_visible(True)

        self.load_directory_files(filepath)

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                md_content = f.read()
        except Exception as e:
            md_content = f"# Error\nFailed to read file: {e}"

        self.render_markdown(md_content, os.path.dirname(filepath))

    def load_directory_files(self, filepath):
        dir_path = os.path.dirname(os.path.abspath(filepath))
        # Clear previous list
        while True:
            row = self.file_list_box.get_row_at_index(0)
            if not row:
                break
            self.file_list_box.remove(row)

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

                self.file_list_box.append(row)

                if os.path.abspath(full_path) == os.path.abspath(filepath):
                    self.file_list_box.select_row(row)
        except Exception as e:
            print(f"Error loading directory files: {e}")

    def render_markdown(self, md_content, parent_dir):
        is_dark = self.style_manager.get_dark()
        theme_val = "dark" if is_dark else "light"
        script_dir = os.path.dirname(os.path.abspath(__file__))
        assets_dir = os.path.join(script_dir, "assets")

        raw_md_json = json.dumps(md_content)

        html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <link rel="stylesheet" href="file://{assets_dir}/github-markdown.min.css">
  <link rel="stylesheet" href="file://{assets_dir}/highlight-github.min.css" id="highlight-light" {"disabled" if is_dark else ""}>
  <link rel="stylesheet" href="file://{assets_dir}/highlight-github-dark.min.css" id="highlight-dark" {"disabled" if not is_dark else ""}>
  <script src="file://{assets_dir}/marked.min.js"></script>
  <script src="file://{assets_dir}/highlight.min.js"></script>
  <script src="file://{assets_dir}/mermaid.min.js"></script>
  <style>
    body {{
      box-sizing: border-box;
      min-width: 200px;
      max-width: 980px;
      margin: 0 auto;
      padding: 45px;
      background-color: var(--color-canvas-default);
    }}
    @media (max-width: 767px) {{
      body {{ padding: 15px; }}
    }}
    .mermaid {{
      background: transparent;
      display: flex;
      justify-content: center;
      margin: 20px 0;
    }}
  </style>
</head>
<body class="markdown-body" data-color-mode="{theme_val}" data-light-theme="light" data-dark-theme="dark">
  <div id="content"></div>
  <div id="error-console" style="color: #a61c1c; background: #fdf2f2; padding: 20px; border: 1px solid #f8b4b4; border-radius: 6px; display: none; font-family: monospace; white-space: pre-wrap; margin: 20px; font-size: 14px;"></div>
  <script>
    try {{
      marked.setOptions({{
        gfm: true,
        breaks: true,
        highlight: function(code, lang) {{
          const language = hljs.getLanguage(lang) ? lang : 'plaintext';
          return hljs.highlight(code, {{ language }}).value;
        }}
      }});

      const markdownText = {raw_md_json};
      const contentDiv = document.getElementById('content');
      contentDiv.innerHTML = marked.parse(markdownText);

      // Extract headings
      const headers = Array.from(contentDiv.querySelectorAll('h1, h2, h3, h4, h5, h6'));
      const outline = headers.map((h, index) => {{
        if (!h.id) {{
          h.id = 'heading-' + index;
        }}
        return {{
          level: parseInt(h.tagName.substring(1)),
          text: h.textContent,
          id: h.id
        }};
      }});
      
      // Post outline
      if (window.webkit && window.webkit.messageHandlers && window.webkit.messageHandlers.outline) {{
        window.webkit.messageHandlers.outline.postMessage(JSON.stringify(outline));
      }}

      // Preprocess and render Mermaid diagrams
      const mermaidCodes = Array.from(contentDiv.querySelectorAll('pre code.language-mermaid'));
      if (mermaidCodes.length > 0) {{
        mermaidCodes.forEach((codeBlock, idx) => {{
          const pre = codeBlock.parentNode;
          const div = document.createElement('div');
          div.className = 'mermaid';
          div.id = 'mermaid-' + idx;
          div.textContent = codeBlock.textContent;
          pre.parentNode.replaceChild(div, pre);
        }});

        mermaid.initialize({{
          startOnLoad: false,
          theme: '{ "dark" if is_dark else "default" }',
          securityLevel: 'loose'
        }});
        mermaid.run();
      }}
    }} catch (err) {{
      const errDiv = document.getElementById('error-console');
      errDiv.style.display = 'block';
      errDiv.textContent = 'JavaScript Error:\\n' + err.message + '\\n\\nStack:\\n' + err.stack;
    }}
  </script>
</body>
</html>
"""
        base_uri = "file://" + urllib.parse.quote(parent_dir, safe='/') + "/"
        self.webview.load_html(html, base_uri)

    def on_outline_received(self, manager, jsc_value):
        try:
            json_str = jsc_value.to_string()
            outline = json.loads(json_str)

            # Clear outline
            while True:
                row = self.outline_list_box.get_row_at_index(0)
                if not row:
                    break
                self.outline_list_box.remove(row)

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
                    label.set_markup(f"<b>{text}</b>")
                else:
                    label.set_text(text)

                row = Gtk.ListBoxRow()
                row.set_child(label)
                row.heading_id = heading_id
                self.outline_list_box.append(row)
        except Exception as e:
            print(f"Error parsing outline: {e}")

    def on_outline_row_activated(self, list_box, row):
        if row and hasattr(row, 'heading_id'):
            js = f"document.getElementById('{row.heading_id}').scrollIntoView({{behavior: 'smooth'}});"
            self.webview.evaluate_javascript(js, -1)

    def on_file_row_activated(self, list_box, row):
        if row and hasattr(row, 'filepath'):
            self.open_file(row.filepath, save_to_history=True)

    def on_decide_policy(self, webview, decision, decision_type):
        if decision_type == WebKit.PolicyDecisionType.NAVIGATION_ACTION:
            action = decision.get_navigation_action()
            request = action.get_request()
            uri = request.get_uri()

            if action.is_user_gesture():
                decision.ignore()
                if uri.startswith("file://"):
                    file_path = urllib.parse.unquote(uri[7:])
                    if file_path.lower().endswith(('.md', '.markdown')):
                        self.open_file(file_path, save_to_history=True)
                    else:
                        Gio.AppInfo.launch_default_for_uri(uri, None)
                elif uri.startswith(("http://", "https://", "mailto:")):
                    Gio.AppInfo.launch_default_for_uri(uri, None)
                return True
        return False

    def on_mouse_button_pressed(self, gesture, n_press, x, y):
        button = gesture.get_current_button()
        if button == 8: # Back mouse button
            self.go_back(None)
            gesture.set_state(Gtk.EventSequenceState.CLAIMED)
        elif button == 9: # Forward mouse button
            self.go_forward(None)
            gesture.set_state(Gtk.EventSequenceState.CLAIMED)

    def go_back(self, btn):
        if self.history_back:
            prev_file = self.history_back.pop()
            if self.current_filepath:
                self.history_forward.append(self.current_filepath)
            self.btn_forward.set_sensitive(True)
            self.btn_back.set_sensitive(len(self.history_back) > 0)
            self.open_file(prev_file, save_to_history=False)

    def go_forward(self, btn):
        if self.history_forward:
            next_file = self.history_forward.pop()
            if self.current_filepath:
                self.history_back.append(self.current_filepath)
            self.btn_back.set_sensitive(True)
            self.btn_forward.set_sensitive(len(self.history_forward) > 0)
            self.open_file(next_file, save_to_history=False)

    def toggle_left_sidebar(self, btn):
        self.file_list_scroll.set_visible(btn.get_active())

    def toggle_right_sidebar(self, btn):
        self.outline_scroll.set_visible(btn.get_active())

    def on_theme_changed(self, manager, gspec):
        if self.current_filepath:
            self.open_file(self.current_filepath, save_to_history=False)
        else:
            self.show_placeholder()

    def show_file_chooser(self):
        dialog = Gtk.FileDialog.new()
        dialog.set_title("Open Markdown File")
        
        if self.current_filepath:
            parent_dir = os.path.dirname(self.current_filepath)
            initial_folder_file = Gio.File.new_for_path(parent_dir)
            dialog.set_initial_folder(initial_folder_file)
        
        filters = Gio.ListStore.new(Gtk.FileFilter)
        
        filter_md = Gtk.FileFilter.new()
        filter_md.set_name("Markdown files")
        filter_md.add_suffix("md")
        filter_md.add_suffix("markdown")
        filters.append(filter_md)
        
        filter_all = Gtk.FileFilter.new()
        filter_all.set_name("All files")
        filter_all.add_pattern("*")
        filters.append(filter_all)
        
        dialog.set_filters(filters)
        dialog.set_default_filter(filter_md)
        dialog.open(self, None, self.on_file_dialog_open_callback)

    def on_file_dialog_open_callback(self, dialog, result):
        try:
            file = dialog.open_finish(result)
            if file:
                self.open_file(file.get_path(), save_to_history=True)
        except Exception as e:
            print(f"Error selecting file: {e}")

class MarkdownViewerApp(Adw.Application):
    def __init__(self):
        super().__init__(
            application_id="com.antiloop.MarkdownViewer",
            flags=Gio.ApplicationFlags.HANDLES_OPEN
        )

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

if __name__ == "__main__":
    GLib.set_prgname("com.antiloop.MarkdownViewer")
    GLib.set_application_name("Antiloop Markdown Viewer")
    app = MarkdownViewerApp()
    sys.exit(app.run(sys.argv))
