import sys
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QSplitter, QTreeView, QFileSystemModel,
    QTabWidget, QMessageBox, QShortcut, QMenu, QAction, QInputDialog, QPushButton, QToolBar,QPlainTextEdit, 
    QLineEdit, QVBoxLayout, QWidget
)
from PyQt5.QtCore import Qt, QDir, QModelIndex, QFileInfo, QFile, QProcess, QCoreApplication, QUrl, QEvent
from PyQt5.Qsci import QsciScintilla, QsciLexerPython, QsciLexerHTML, QsciLexerCSS
from PyQt5.QtGui import QColor, QFont, QKeySequence
import yaml
import os
from PyQt5.QtWebEngineWidgets import QWebEngineView
from win32api import GetSystemMetrics
import PyInstaller.__main__




with open(f'{os.path.dirname(os.path.realpath(__file__))}/config.yaml', 'r') as file:
    data = yaml.safe_load(file)


global textsize
global terminal_type
global caret_fg_color
global curserwidth
global backgroundcolor
global scrollbarbackgorund
global fileexplorerbacgroundcolor
global mainbacgroundcolor
global linenumbersbackground
global linenumberstextbackground
textsize=data['font_size']
terminal_type=data['terminal_type']
caret_fg_color = QColor(str(data['caret_fg_color']))
curserwidth=data['curserwidth']
backgroundcolor=QColor(str(data['backgroundcolor']))
scrollbarbackgorund=data['scrollbarbackgorund']
fileexplorerbacgroundcolor=data['fileexplorerbacgroundcolor']
mainbacgroundcolor=data['mainbacgroundcolor']
linenumbersbackground=QColor(str(data['linenumbersbackground']))
linenumberstextbackground=QColor(str(data['linenumberstextbackground']))
save_shortcut_keybind=data['save_shortcut']
run_shortcut_keybind=data['run_shortcut']
compile_shortcut_keybind=data['compile_shortcut']
open_settings_menu_keybind=data['open_settings']

Hilight_current_line_color=QColor(str(data['current_line']))



from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton, QColorDialog, QComboBox, QSpinBox, QLabel
from PyQt5.QtGui import QColor
import yaml

class HTMLViewerWidget(QWidget):
    def __init__(self, file_path, parent=None):
        super().__init__(parent)
        self.file_path = file_path
        layout = QVBoxLayout(self)
        self.web_view = QWebEngineView()
        layout.addWidget(self.web_view)
        self.web_view.setUrl(QUrl.fromLocalFile(file_path))
        self.setLayout(layout)

    def close_viewer(self):
        pass

    def load_html_file(self):
        self.web_view.setUrl(QUrl.fromLocalFile(self.file_path))

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.layout = QFormLayout()
        self.font_size_spinbox = QSpinBox()
        self.font_size_spinbox.setValue(data['font_size'])
        self.layout.addRow(QLabel("Font Size:"), self.font_size_spinbox)
        self.terminal_type_combobox = QComboBox()
        self.terminal_type_combobox.addItems(['cmd', 'powershell'])
        self.terminal_type_combobox.setCurrentText(data['terminal_type'])
        self.layout.addRow(QLabel("Terminal Type:"), self.terminal_type_combobox)

        self.colors = {
            'Curser Color': 'caret_fg_color',
            'Textbox Color': 'backgroundcolor',
            'Scrollbar Color': 'scrollbarbackgorund',
            'File Explorer Color': 'fileexplorerbacgroundcolor',
            'Main Background Color': 'mainbacgroundcolor',
            'Line Numbers color': 'linenumbersbackground',
            'Line Numbers Text Color': 'linenumberstextbackground',

			'Hilight Current Line Color': 'current_line'
        }

        self.color_buttons = {}
        for label, key in self.colors.items():
            button = QPushButton()
            button.setStyleSheet(f"background-color: {data[key]};")
            button.clicked.connect(lambda _, k=key: self.pick_color(k))
            self.layout.addRow(QLabel(label + ":"), button)
            self.color_buttons[key] = button

        self.keybindings = {
            'Save': 'save_shortcut',
            'Run': 'run_shortcut',
            'Compile': 'compile_shortcut',
            'Settings': 'open_settings'
        }

        self.keybinding_inputs = {}
        for label, key in self.keybindings.items():
            button = QLineEdit()
            if label == 'Save':
                button.setPlaceholderText(f"{save_shortcut_keybind} Press keys...")
            elif label == "Run":
                button.setPlaceholderText(f"{run_shortcut_keybind} Press keys...")
            elif label == "Compile":
                button.setPlaceholderText(f"{compile_shortcut_keybind} Press keys...")
            elif label == "Settings":
                button.setPlaceholderText(f"{open_settings_menu_keybind} Press keys...")
            button.setReadOnly(True)
            button.installEventFilter(self)
            self.layout.addRow(QLabel(f"{label} Shortcut:"), button)
            self.keybinding_inputs[key] = button

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_settings)
        self.layout.addRow(self.save_button)

        self.setLayout(self.layout)


    def eventFilter(self, source, event):
        if event.type() == QEvent.KeyPress and source in self.keybinding_inputs.values():
            keys = []
            if event.modifiers() & Qt.ControlModifier:
                keys.append('Ctrl')
            if event.modifiers() & Qt.AltModifier:
                keys.append('Alt')
            if event.modifiers() & Qt.ShiftModifier:
                keys.append('Shift')
            keys.append(QKeySequence(event.key()).toString())
            source.setText('+'.join(keys))
            return True
        return super().eventFilter(source, event)

    def save_settings(self):
        data['font_size'] = self.font_size_spinbox.value()
        data['terminal_type'] = self.terminal_type_combobox.currentText()
        for key, input_widget in self.keybinding_inputs.items():
            send=input_widget.text()
            if key == 'save_shortcut' and input_widget.text() =='':
                send=save_shortcut_keybind
            if key == 'run_shortcut' and input_widget.text() =='':
                send=run_shortcut_keybind
            if key == 'compile_shortcut' and input_widget.text() =='':
                send=compile_shortcut_keybind
            if key == 'open_settings' and input_widget.text() =='':
                send=open_settings_menu_keybind
            data[key] = send
        with open('config.yaml', 'w') as file:
            yaml.dump(data, file)
        QMessageBox.information(self, "Settings", "Settings have been saved.")
        self.restart_application()

    def pick_color(self, key):
        color = QColorDialog.getColor(QColor(data[key]), self)
        if color.isValid():
            self.color_buttons[key].setStyleSheet(f"background-color: {color.name()};")
            data[key] = color.name()

    def restart_application(self):
        """Restart the application."""
        script = os.path.abspath(sys.argv[0])
        subprocess.Popen([sys.executable, script])
        QCoreApplication.quit()




        



class CodeEditor(QsciScintilla):
    def __init__(self, file_path='', parent=None):
        super().__init__(parent)
        self.file_path = file_path
        self.is_modified = False
        font = QFont()
        font.setFamily('Cascadia Code')
        font.setFixedPitch(True)
        font.setPointSize(textsize)
        self.setFont(font)
        self.setMarginsFont(font)
        self.setUtf8(True)
        self.setCaretForegroundColor(caret_fg_color)
        self.setCaretLineVisible(True)
        self.setCaretWidth(curserwidth)
        self.setTabWidth(4)
        if file_path.endswith('.py') or file_path.endswith('.python'):
            self.lexer = QsciLexerPython()
            self.lexer.setDefaultFont(font)
            self.setLexer(self.lexer)

            self.lexer.setPaper(backgroundcolor)
    
            self.lexer.setColor(QColor("#FF0000"), QsciLexerPython.Identifier)  
            self.lexer.setColor(QColor("#4ec9b0"), QsciLexerPython.FunctionMethodName)  
            
            self.lexer.setFont(font, QsciLexerPython.Identifier)
            self.lexer.setFont(font, QsciLexerPython.FunctionMethodName)

        elif file_path.endswith('.html'):
            self.lexer = QsciLexerHTML()
            self.lexer.setDefaultFont(font)
            self.setLexer(self.lexer)

            self.lexer.setPaper(backgroundcolor)
        
        elif file_path.endswith('.css'):
            self.lexer = QsciLexerCSS()
            self.lexer.setDefaultFont(font)
            self.setLexer(self.lexer)

            self.lexer.setPaper(backgroundcolor)

        self.setMarginsBackgroundColor(linenumbersbackground)
        self.setMarginsForegroundColor(linenumberstextbackground)
        self.setMarginWidth(0, "0000")
        self.setMarginLineNumbers(0, True)
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)
        self.setAutoIndent(True)
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(Hilight_current_line_color)
        self.setStyleSheet(f"background-color: {scrollbarbackgorund};")
        self.setPaper(backgroundcolor)
        self.textChanged.connect(self.on_text_changed)

    def load_file(self, file_path):
        self.file_path = file_path
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                self.setText(content)
                self.is_modified = False
                self.update_window_title()
        except Exception as e:
            raise RuntimeError(f"Cannot load file: {str(e)}")

    def on_text_changed(self):
        if not self.is_modified:
            self.is_modified = True
            self.update_window_title()

    def save_file(self):
        if self.file_path:
            with open(self.file_path, 'w') as file:
                file.write(self.text())
            self.is_modified = False
            self.update_window_title()
            return True
        return False

    def update_window_title(self):
        file_name = QFileInfo(self.file_path).fileName()
        if self.is_modified:
            self.setWindowTitle(f'*{file_name}')
        else:
            self.setWindowTitle(file_name)

class TerminalWidget(QWidget):
    def __init__(self, file_path, command=None, parent=None):
        super().__init__(parent)
        self.file_path = file_path
        self.command = command or ["python", file_path]  # Default command to run
        self.terminal_type = terminal_type
        self.process = QProcess(self)
        self.process.setProcessChannelMode(QProcess.MergedChannels)

        self.output_area = QPlainTextEdit()
        self.output_area.setReadOnly(True)
        
        self.input_area = QLineEdit()
        self.input_area.returnPressed.connect(self.send_command)

        layout = QVBoxLayout()
        layout.addWidget(self.output_area)
        layout.addWidget(self.input_area)
        self.setLayout(layout)

        self.setup_terminal()

    def setup_terminal(self):
        # Extract the directory from the file_path
        working_directory = QFileInfo(self.file_path).absolutePath()
        print(working_directory)
        self.process.setWorkingDirectory(working_directory)  # Set the working directory

        if self.terminal_type == 'cmd':
            self.process.start("cmd.exe", ['/c'] + self.command)
        elif self.terminal_type == 'powershell':
            self.process.start("powershell.exe", ['-Command'] + self.command)

        self.process.readyRead.connect(self.read_output)
        self.process.errorOccurred.connect(self.handle_error)
        self.process.finished.connect(self.process_finished)

    def send_command(self):
        command = self.input_area.text()
        self.process.write(command.encode() + b'\n')
        self.input_area.clear()

    def read_output(self):
        output = self.process.readAll().data().decode()
        self.output_area.appendPlainText(output)

    def handle_error(self, error):
        self.output_area.appendPlainText(f"Error: {error}")

    def process_finished(self):
        self.output_area.appendPlainText("Process finished.")

    def close_terminal(self):
        self.process.terminate()
        self.process.waitForFinished()



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()


        # Create a file tree view on the left side
        self.file_tree = FileTreeView()
        self.file_model = QFileSystemModel()
        self.file_model.setRootPath(os.path.dirname(os.path.realpath(__file__)) + "/projects")
        self.file_tree.setModel(self.file_model)
        self.file_tree.setRootIndex(self.file_model.index(os.path.dirname(os.path.realpath(__file__)) + "/projects"))
        self.file_tree.setColumnWidth(0, 250)
        self.file_tree.setSortingEnabled(True)
        self.file_tree.setHeaderHidden(True)

        # Connect the file tree click event to open the file
        self.file_tree.clicked.connect(self.on_file_tree_clicked)

        # Tab widget for multiple open files
        self.file_tabs = QTabWidget()
        self.file_tabs.setTabsClosable(True)
        self.file_tabs.tabCloseRequested.connect(self.close_file_tab)

        # Tab widget for terminals
        self.terminal_tabs = QTabWidget()
        self.terminal_tabs.setTabsClosable(True)
        self.terminal_tabs.tabCloseRequested.connect(self.close_terminal_tab)

        # Create a splitter to separate file tree and the central area
        self.splitter1 = QSplitter(Qt.Horizontal)
        self.splitter1.addWidget(self.file_tabs)
        self.splitter1.addWidget(self.file_tree)
        self.splitter1.setStretchFactor(0, 8)
        self.splitter1.setStretchFactor(1, 2) 

        # Create a main layout for the terminal area and file editor
        self.splitter2 = QSplitter(Qt.Vertical)
        self.splitter2.addWidget(self.splitter1)
        self.splitter2.addWidget(self.terminal_tabs)
        self.splitter2.setStretchFactor(0, 4)  # Main content
        self.splitter2.setStretchFactor(1, 1)  # Terminals

        # Create a central widget and set the layout
        central_widget = QWidget()
        central_widget.setLayout(QVBoxLayout())
        central_widget.layout().addWidget(self.splitter2)
        
        self.setCentralWidget(central_widget)

        # Create a toolbar for the run button and add it to the title bar
        self.toolbar = QToolBar("Main Toolbar")
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)

        # Create and add the run button to the toolbar
        self.run_button = QPushButton('Run')
        self.run_button.clicked.connect(self.run_current_file)
        self.toolbar.addWidget(self.run_button)

        self.compile_button = QPushButton('Compile')
        self.compile_button.clicked.connect(self.compile_current_file)
        self.toolbar.addWidget(self.compile_button)

       # Load keybindings
        self.save_shortcut = QShortcut(QKeySequence(save_shortcut_keybind), self)
        self.save_shortcut.activated.connect(self.save_current_tab)

        self.run_shortcut = QShortcut(QKeySequence(run_shortcut_keybind), self)
        self.run_shortcut.activated.connect(self.run_current_file)

        self.compile_shortcut = QShortcut(QKeySequence(compile_shortcut_keybind), self)
        self.compile_shortcut.activated.connect(self.compile_current_file)

        self.open_settings_menu = QShortcut(QKeySequence(open_settings_menu_keybind), self)
        self.open_settings_menu.activated.connect(self.open_settings)

        self.setStyleSheet(f"background-color: {mainbacgroundcolor};")

        self.setWindowTitle("RKing Editor")


        self.resize(int(GetSystemMetrics(0)//1.3), int(GetSystemMetrics(1)//1.3))

        # Open the default file at startup
        self.open_default_file()
        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.open_settings)
        self.toolbar.addAction(settings_action)

    def open_settings(self):
        dialog = SettingsDialog(self)
        dialog.exec_()

    def open_default_file(self):
        # Define the path to the default file
        default_file_path = os.path.dirname(os.path.realpath(__file__)) + "/introduction.txt"
        if QFileInfo(default_file_path).exists():
            self.open_file_in_tab(default_file_path)

    def on_file_tree_clicked(self, index: QModelIndex):
        # Get the file path from the model
        file_path = self.file_model.filePath(index)
        
        # Check if the clicked item is a file
        if not self.file_model.isDir(index):
            self.open_file_in_tab(file_path)

    def open_file_in_tab(self, file_path):
        # Extract just the file name from the path
        file_name = QFileInfo(file_path).fileName()

        # Check if the file is already open in a tab
        for i in range(self.file_tabs.count()):
            if self.file_tabs.tabText(i).startswith(file_name):
                self.file_tabs.setCurrentIndex(i)
                return

        # Create a new editor for the file
        try:
            editor = CodeEditor(file_path)
            editor.load_file(file_path)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Cannot display file format: {str(e)}")
            return

        # Add the new editor to a new tab with just the file name
        self.file_tabs.addTab(editor, file_name)
        self.file_tabs.setCurrentWidget(editor)

    def close_file_tab(self, index):
        tab_widget = self.file_tabs.widget(index)
        if isinstance(tab_widget, CodeEditor) and tab_widget.is_modified:
            # Ask user if they want to save changes
            response = QMessageBox.question(
                self, 'Unsaved Changes', 
                'The file has unsaved changes. Do you want to save them?',
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
            )
            if response == QMessageBox.Yes:
                if not tab_widget.save_file():
                    return  # Abort closing if saving fails
            elif response == QMessageBox.Cancel:
                return  # Abort closing if user cancels

        self.file_tabs.removeTab(index)

    def save_current_tab(self):
        # Get the current widget (CodeEditor) in the tab
        current_widget = self.file_tabs.currentWidget()
        if isinstance(current_widget, CodeEditor):
            current_widget.save_file()

    def run_current_file(self):
        current_widget = self.file_tabs.currentWidget()
        if isinstance(current_widget, CodeEditor):
            file_path = current_widget.file_path
            if file_path.endswith('py') or file_path.endswith('python'):
                if QFileInfo(file_path).exists():
                    terminal_widget = TerminalWidget(file_path)
                    self.terminal_tabs.addTab(terminal_widget, QFileInfo(file_path).fileName())
                    self.terminal_tabs.setCurrentWidget(terminal_widget)
            elif file_path.endswith('html'):
                self.run_html_file(file_path)

    def run_html_file(self, file_path):
        if QFileInfo(file_path).exists():
            html_viewer_widget = HTMLViewerWidget(file_path)
            self.terminal_tabs.addTab(html_viewer_widget, f"HTML: {QFileInfo(file_path).fileName()}")
            self.terminal_tabs.setCurrentWidget(html_viewer_widget)

    def close_terminal_tab(self, index):
        terminal_widget = self.terminal_tabs.widget(index)
        if isinstance(terminal_widget, TerminalWidget):
            terminal_widget.close_terminal()
        elif isinstance(terminal_widget, HTMLViewerWidget):
            terminal_widget.close_viewer()  # Close the HTML viewer if necessary
        self.terminal_tabs.removeTab(index)

    def compile_current_file(self):
        current_widget = self.file_tabs.currentWidget()
        if isinstance(current_widget, CodeEditor):
            file_path = current_widget.file_path
            if file_path.endswith('py') or file_path.endswith('python'):
                if QFileInfo(file_path).exists():
                    # Determine the directory of the file
                    working_directory = QFileInfo(file_path).absolutePath()
                    # Create a new terminal widget
                    
                    terminal_widget = TerminalWidget(file_path, command=['python', '-m', 'PyInstaller', file_path])
                    terminal_widget.process.setWorkingDirectory(working_directory)
                    # Add the terminal widget as a new tab
                    self.terminal_tabs.addTab(terminal_widget, f"Compile {QFileInfo(file_path).fileName()}")
                    self.terminal_tabs.setCurrentWidget(terminal_widget)





class FileTreeView(QTreeView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        
        # Initialize the actions
        self.create_file_action = QAction("Create File", self)
        self.create_folder_action = QAction("Create Folder", self)
        self.rename_action = QAction("Rename", self)
        self.delete_action = QAction("Delete", self)
        self.create_project_action = QAction("Create Project", self)

        # Connect actions to slots
        self.create_file_action.triggered.connect(self.create_file)
        self.create_folder_action.triggered.connect(self.create_folder)
        self.rename_action.triggered.connect(self.rename_item)
        self.delete_action.triggered.connect(self.delete_item)
        self.create_project_action.triggered.connect(self.create_project)

        self.setStyleSheet(f"background-color: {fileexplorerbacgroundcolor};")

    def show_context_menu(self, pos):
        index = self.indexAt(pos)
        self.menu = QMenu(self)
        if index.isValid():
            # Item is clicked
            if self.model().isDir(index):
                # Right-clicked on a folder
                self.menu.addAction(self.create_file_action)  # Option to create a file
                self.menu.addAction(self.create_folder_action)  # Option to create a folder
                self.menu.addAction(self.rename_action)  # Option to rename
                self.menu.addAction(self.delete_action)  # Option to delete
            else:
                # Right-clicked on a file
                self.menu.addAction(self.rename_action)  # Option to rename
                self.menu.addAction(self.delete_action)  # Option to delete
        else:
            # Right-clicked on empty space
            self.menu.addAction(self.create_project_action)  # Option to create a project

        # Show the context menu
        self.menu.exec_(self.viewport().mapToGlobal(pos))

    def create_file(self):
        index = self.currentIndex()
        if index.isValid() and self.model().isDir(index):
            path = self.model().filePath(index)
            file_name, _ = QInputDialog.getText(self, "Create File", "File name:")
            if file_name:
                file_path = QDir(path).filePath(file_name)
                with open(file_path, 'w') as f:
                    pass
                self.refresh_model()

    def create_folder(self):
        index = self.currentIndex()
        if index.isValid() and self.model().isDir(index):
            path = self.model().filePath(index)
            folder_name, _ = QInputDialog.getText(self, "Create Folder", "Folder name:")
            if folder_name:
                new_folder_path = QDir(path).filePath(folder_name)
                QDir().mkdir(new_folder_path)
                self.refresh_model()

    def rename_item(self):
        index = self.currentIndex()
        if index.isValid():
            old_name = self.model().filePath(index)
            new_name, _ = QInputDialog.getText(self, "Rename", "New name:")
            if new_name:
                new_name_path = QDir(QFileInfo(old_name).path()).filePath(new_name)
                if QFileInfo(old_name).isDir():
                    QDir().rename(old_name, new_name_path)
                else:
                    QFile().rename(old_name, new_name_path)
                self.refresh_model()

    def delete_item(self):
        index = self.currentIndex()
        if index.isValid():
            file_path = self.model().filePath(index)
            reply = QMessageBox.question(
                self, 'Delete', f"Are you sure you want to delete '{file_path}'?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                if QFileInfo(file_path).isDir():
                    if self.remove_directory(file_path):  # Recursively remove the directory
                        self.refresh_model()
                else:
                    if QFile(file_path).remove():  # Remove the file
                        self.refresh_model()

    def remove_directory(self, dir_path):
        dir = QDir(dir_path)
        if not dir.exists():
            return False

        # Recursively delete all contents
        for entry in dir.entryList(QDir.AllEntries | QDir.NoDotAndDotDot):
            entry_path = dir.filePath(entry)
            if QDir(entry_path).exists():
                if not self.remove_directory(entry_path):  # Recursive call for subdirectories
                    return False
            else:
                if not QFile(entry_path).remove():
                    return False

        return dir.rmdir(dir_path)  # Finally, remove the directory itself

    def refresh_model(self):
        # Refresh the model by resetting the root path
        root_path = self.model().rootPath()
        self.model().setRootPath('')
        self.model().setRootPath(root_path)

    def create_project(self):
        path = self.model().rootPath()  # Or any other default directory you want
        project_name, _ = QInputDialog.getText(self, "Create Project", "Project name:")
        if project_name:
            project_path = QDir(path).filePath(project_name)
            if QDir().mkdir(project_path):
                self.refresh_model()
            else:
                QMessageBox.warning(self, "Error", "Failed to create project folder.")






if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())