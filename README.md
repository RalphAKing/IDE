# RKing Editor

RKing Editor is a versatile project management and code editing tool. It features an intuitive user interface, file management capabilities, terminal integration, and HTML viewing, making it an ideal choice for developers working on multi-language projects.

## Key Features

### File Explorer
- **Tree View:** Displays project files and directories.
- **Context Menu:** Right-click to create, rename, or delete files and folders.
- **Project Management:** Create new projects directly from the file explorer.

### Code Editor
- **File Editing:** Supports opening, editing, and saving files.
- **Unsaved Changes Prompt:** Notifies users to save changes before closing tabs.
- **Customizable Syntax Highlighting (future scope):** Planned for enhancing readability.

### Terminal Integration
- **Run Python and HTML Files:** Execute Python scripts or preview HTML files.
- **Command Execution:** Run commands in CMD or PowerShell.
- **Real-time Output:** Displays terminal output and accepts user input.

### HTML Viewer
- **Preview HTML Files:** Opens HTML files in a dedicated viewer tab.

### Toolbar and Shortcuts
- **Quick Actions:** Buttons for saving, running, and compiling files.
- **Configurable Shortcuts:** Includes hotkeys for frequent actions like saving and running files.

### Tab Management
- **Separate Tabs:** Manage code editor and terminal sessions independently.
- **Closable Tabs:** Close tabs with unsaved changes prompts.

### Settings
- **Customization:** Access a settings dialog to configure application preferences.
- **Appearance:** Set custom background colors for the editor and file explorer.

### Default Behavior
- **Auto-load Introduction File:** Automatically opens `introduction.txt` in the `/projects` directory if it exists.

## Usage

1. **File Management:**
   - Navigate the file explorer to open or create new files and projects.
   - Right-click on files or directories for additional options.

2. **Editing Files:**
   - Open a file in the editor by clicking on it in the file explorer.
   - Save changes using the toolbar button or shortcut.

3. **Running Files:**
   - Click the "Run" button in the toolbar to execute Python or HTML files.
   - View the output in a dedicated terminal or HTML viewer tab.

4. **Compiling Files:**
   - Click the "Compile" button to package Python files using PyInstaller.

## Customization

### Keyboard Shortcuts
- Configure the following shortcuts in the settings:
  - Save file
  - Run file
  - Compile file
  - Open settings menu

### Appearance
- Change the background color of the editor and file explorer in the settings dialog.

## Planned Features
- **Syntax Highlighting:** Add language-specific syntax highlighting.
- **Search Functionality:** Implement a search bar for quick navigation.
- **Additional Language Support:** Expand support to C++, Java, and other languages.

## Contributing

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-branch
   ```
3. Commit your changes:
   ```bash
   git commit -m 'Add new feature'
   ```
4. Push the branch:
   ```bash
   git push origin feature-branch
   ```
5. Open a pull request.


## License

This project is open-source and available for modification and use under the MIT license.

### MIT License

```
MIT License

Copyright (c) 2024 Ralph King

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
```
