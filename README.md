# Antiloop Markdown Viewer

A premium, offline-first Markdown viewer built specifically for the GNOME desktop environment using **Python 3**, **GTK4**, **Libadwaita**, and **WebKit**. 

It provides a native GTK look and feel, fits perfectly into your GNOME environment, and supports advanced formatting features like tables, code syntax highlighting, and Mermaid diagrams—all fully offline.

![Antiloop Markdown Viewer Screenshot](screenshot.png)

## Core Features

*   📂 **Double Sidebars**:
    *   **Left Sidebar**: File browser showing all Markdown files in the folder of the opened file for quick document switching.
    *   **Right Sidebar**: Interactive document outline automatically generated from headings, allowing smooth scrolling to sections.
*   🔄 **History Navigation**: Move back and forward through visited files using the header bar navigation buttons or your mouse's side buttons (Button 8 and 9).
*   🌓 **Theme Synchronization**: Listens to system settings and automatically switches between light and dark modes.
*   📊 **Offline Mermaid Diagrams**: Full client-side offline rendering of flowcharts, sequence diagrams, class diagrams, and Gantt charts.
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
| **`Ctrl + W`** | Close the current window |
| **`Ctrl + Q`** | Quit the application |

---

*Developed by Antiloop GmbH.*
