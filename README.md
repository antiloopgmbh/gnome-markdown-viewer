# Antiloop Markdown Viewer

A premium, offline-first Markdown viewer built specifically for the GNOME desktop environment using **Python 3**, **GTK4**, **Libadwaita**, and **WebKit**. 

It provides a native GTK look and feel, fits perfectly into your GNOME environment, and supports advanced formatting features like tables, code syntax highlighting, and Mermaid diagrams—all fully offline.

![Antiloop Markdown Viewer Screenshot](screenshot.png)

## Core Features

*   📂 **Double Sidebars & Persistent States**:
    *   **Left Sidebar (File/Directory Explorer)**: Live tree-like directory browser displaying folders first (with folder icons) and Markdown files (with document icons) alphabetically. Supports deep folder navigation.
    *   **Right Sidebar (Document Outline)**: Interactive document outline automatically generated from headings, allowing smooth scrolling to sections.
    *   **Persisted Layout**: Remembers the open/closed visibility states of both sidebars across file switches and application restarts.
*   🔄 **Automatic Reopening & Recent Files**:
    *   Restores the last opened document automatically on application startup.
    *   Dropdown menu in the header bar showing the last 10 explicitly opened files with styled filenames and ellipsized directory paths.
*   ⚡ **Live Hot-Reloading & File/Folder Monitoring**:
    *   **Live Document Reload**: Watches the currently open file and automatically refreshes the viewer when it is modified on disk.
    *   **Live Sidebar Update**: Monitors the directory for changes, updating the files and folders list in real-time as items are added, deleted, or renamed.
*   📊 **Full-Width Canvas & Premium Formatting**:
    *   Responsive, 100% full-width document canvas allowing wide Mermaid diagrams (flowcharts, sequence diagrams, Gantt charts, etc.) and tables to scale up and remain fully legible.
    *   Theme-synchronized, clean table header styles.
*   🔍 **Flatpak Portal Path Resolution**:
    *   Translates sandboxed portal paths (`/run/user/...`) to their real host paths on launch via FUSE extended attributes (`xattr::document-portal.host-path`). This unlocks access to relative images and folder lists even when the app is started from file managers or CLI.
*   🌓 **Theme Synchronization**: Listens to system settings and automatically switches between light and dark modes.
*   💻 **Syntax Highlighting**: Real-time theme-synchronized code formatting for multiple languages (Python, JavaScript, YAML, etc.).
*   🔒 **Secure Sandbox (Flatpak)**: Runs in an isolated Flatpak container with minimum required permissions.

---

## Installation & Running (Flatpak)

Building and running the application in a secure sandbox.

1. **Install Flatpak-Builder and SDK**:
   ```bash
   sudo dnf install -y flatpak-builder
   flatpak install flathub org.gnome.Sdk//47 org.gnome.Platform//47
   ```
2. **Build and Install Locally**:
   ```bash
   flatpak-builder --user --install --force-clean build-dir com.antiloop.MarkdownViewer.yml
   ```
3. **Launch the Application**:
   You can launch the app from your GNOME Application menu or via terminal:
   ```bash
   flatpak run com.antiloop.MarkdownViewer
   ```

---

## Keyboard Shortcuts

| Shortcut | Description |
| :---: | :--- |
| **`Ctrl + O`** | Open a new Markdown file |
| **`Ctrl + W`** | Close the current document (returns to placeholder screen) |
| **`Ctrl + Q`** | Quit the application |
| **`Mouse Back/Forward`** | Navigate back/forward through document history |

---

*Developed by Antiloop GmbH.*
