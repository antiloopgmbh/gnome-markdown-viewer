#!/bin/bash
set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Target directories
APP_DIR="$HOME/.local/share/applications"
ICON_DIR="$HOME/.local/share/icons/hicolor/scalable/apps"

mkdir -p "$APP_DIR"
mkdir -p "$ICON_DIR"

# Remove old desktop entries if they exist
rm -f "$APP_DIR/linux-md-viewer.desktop"
rm -f "$APP_DIR/org.gnome.MarkdownViewer.desktop"

# Generate local desktop entry with absolute path (using App ID com.antiloop.MarkdownViewer)
cat <<EOF > "$APP_DIR/com.antiloop.MarkdownViewer.desktop"
[Desktop Entry]
Name=Antiloop Markdown Viewer
Comment=Native Markdown viewer for GNOME
Exec=/usr/bin/python3 $SCRIPT_DIR/md_viewer.py %U
Icon=com.antiloop.MarkdownViewer
Terminal=false
Type=Application
Categories=Office;WordProcessor;Utility;
MimeType=text/markdown;text/x-markdown;
StartupNotify=true
EOF

# Copy Icon to multiple standard locations scanned by GNOME
cp "$SCRIPT_DIR/com.antiloop.MarkdownViewer.svg" "$ICON_DIR/"

mkdir -p "$HOME/.local/share/icons"
cp "$SCRIPT_DIR/com.antiloop.MarkdownViewer.svg" "$HOME/.local/share/icons/"

mkdir -p "$HOME/.icons"
cp "$SCRIPT_DIR/com.antiloop.MarkdownViewer.svg" "$HOME/.icons/"

# Clean up old icons
rm -f "$ICON_DIR/linux-md-viewer.svg"
rm -f "$HOME/.local/share/icons/linux-md-viewer.svg"
rm -f "$HOME/.icons/linux-md-viewer.svg"
rm -f "$ICON_DIR/org.gnome.MarkdownViewer.svg"
rm -f "$HOME/.local/share/icons/org.gnome.MarkdownViewer.svg"
rm -f "$HOME/.icons/org.gnome.MarkdownViewer.svg"

# Update desktop and icon databases
update-desktop-database "$APP_DIR" || true
gtk-update-icon-cache -f -t "$HOME/.local/share/icons/hicolor" || true

# Make execution script executable
chmod +x "$SCRIPT_DIR/md_viewer.py"

echo "Installation complete. You can now launch Antiloop Markdown Viewer from your GNOME Applications launcher."
