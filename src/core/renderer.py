import os
import json

def get_template_path():
    # This file is in src/core/renderer.py, so parent of parent is src/
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(script_dir, "assets", "template.html")

def render_markdown(md_content, is_dark, assets_dir):
    template_path = get_template_path()
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()
    except Exception as e:
        return f"<html><body><h2>Error loading template</h2><p>{e}</p></body></html>"

    theme_val = "dark" if is_dark else "light"
    light_disabled = "disabled" if is_dark else ""
    dark_disabled = "disabled" if not is_dark else ""
    mermaid_theme = "dark" if is_dark else "default"
    # Rewrite absolute file:/// URLs to app-local:/// to bypass WebKit cross-origin restrictions
    md_content = md_content.replace("file:///", "app-local:///")
    raw_md_json = json.dumps(md_content)

    html = template
    html = html.replace("{{ASSETS_DIR}}", assets_dir)
    html = html.replace("{{LIGHT_DISABLED}}", light_disabled)
    html = html.replace("{{DARK_DISABLED}}", dark_disabled)
    html = html.replace("{{THEME}}", theme_val)
    html = html.replace("{{MARKDOWN_JSON}}", raw_md_json)
    html = html.replace("{{MERMAID_THEME}}", mermaid_theme)

    return html
