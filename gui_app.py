import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLineEdit, QPushButton, QTextEdit,
                             QLabel, QSplitter, QMessageBox, QFrame, QProgressBar,
                             QStackedWidget, QFileDialog)
from PyQt5.QtCore import Qt, pyqtSignal, QThread
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor

# --- Import the processing function ---
# Make sure extract_and_summarize.py is in the same directory
try:
    from extract_and_summarize import extract_and_summarize
except ImportError:
    # Provide a fallback if the file is missing, to prevent crashing
    def extract_and_summarize(url):
        raise ImportError("Could not find 'extract_and_summarize.py'. Please create it.")


# ==============================================================================
#  CUSTOM STYLED WIDGETS
# ==============================================================================

class ThemedButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton {
                background-color: #009688; /* Teal */
                color: white;
                border: none;
                padding: 10px 22px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #00a99d;
            }
            QPushButton:pressed {
                background-color: #00796b;
            }
            QPushButton:disabled {
                background-color: #4a4a4a;
                color: #9e9e9e;
            }
        """)

class ThemedLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 1px solid #424242;
                border-radius: 6px;
                font-size: 14px;
                background-color: #2d2d2d;
                color: #e0e0e0;
            }
            QLineEdit:focus {
                border: 1px solid #009688; /* Teal */
                background-color: #363636;
            }
        """)

class ThemedTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QTextEdit {
                border: 1px solid #424242;
                border-radius: 6px;
                padding: 10px;
                background-color: #2d2d2d;
                color: #e0e0e0;
                font-size: 14px;
            }
            QScrollBar:vertical {
                border: none;
                background: #2d2d2d;
                width: 12px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #4a4a4a;
                min-height: 20px;
                border-radius: 6px;
            }
        """)

class TitleLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QLabel {
                color: #e0e0e0;
                font-size: 24px;
                font-weight: bold;
            }
        """)

class SectionLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QLabel {
                color: #c0c0c0;
                font-size: 16px;
                font-weight: bold;
                padding-bottom: 5px;
            }
        """)

# ==============================================================================
#  PROCESSING THREAD (REFACTORED)
# ==============================================================================

class ProcessingThread(QThread):
    # Signal now emits raw_content, summary, and a possible error string
    finished = pyqtSignal(str, str, str)

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        try:
            raw_content, summary = extract_and_summarize(self.url)
            self.finished.emit(raw_content, summary, "")  # Success, no error
        except Exception as e:
            self.finished.emit("", "", str(e)) # Failure, send error message

# ==============================================================================
#  MAIN APPLICATION WINDOW
# ==============================================================================

class WebsiteSummarizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Website Summarizer")
        self.setMinimumSize(1200, 800)
        self.setWindowIcon(QIcon.fromTheme("applications-internet"))

        # --- Global App Styling ---
        self.setStyleSheet("""
            QMainWindow { background-color: #1e1e1e; }
            QSplitter::handle { background-color: #424242; }
            QSplitter::handle:horizontal { width: 2px; }
            QMessageBox { background-color: #2d2d2d; }
            QMessageBox QLabel { color: #e0e0e0; font-size: 14px; }
            QMessageBox QPushButton { /* Uses ThemedButton style */ }
            QProgressBar {
                border: 1px solid #424242;
                border-radius: 6px;
                text-align: center;
                color: #e0e0e0;
                background-color: #2d2d2d;
            }
            QProgressBar::chunk {
                background-color: #009688; /* Teal */
                border-radius: 5px;
            }
        """)

        # --- Main Layout ---
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        self.layout = QVBoxLayout(main_widget)
        self.layout.setSpacing(20)
        self.layout.setContentsMargins(25, 25, 25, 25)

        # --- Header ---
        header_layout = QHBoxLayout()
        header_layout.addWidget(TitleLabel("Website Content Summarizer"))
        header_layout.addStretch()

        # --- URL Input Section ---
        url_frame = QFrame()
        url_frame.setStyleSheet("background-color: #2d2d2d; border-radius: 8px;")
        url_layout = QHBoxLayout(url_frame)
        url_layout.setContentsMargins(15, 15, 15, 15)

        self.url_input = ThemedLineEdit()
        self.url_input.setPlaceholderText("Enter website URL and press Enter...")
        self.url_input.returnPressed.connect(self.start_processing)

        self.load_button = ThemedButton("Summarize")
        self.load_button.setIcon(QIcon.fromTheme("document-open-remote"))
        self.load_button.clicked.connect(self.start_processing)
        
        url_layout.addWidget(self.url_input, 1) # Give line edit more space
        url_layout.addWidget(self.load_button)

        # --- Progress Bar ---
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setRange(0, 0)  # Indeterminate

        # --- Content Area (Stacked Widget for Empty State) ---
        self.stacked_widget = QStackedWidget()
        self.create_results_widget()
        self.create_empty_state_widget()
        self.stacked_widget.addWidget(self.empty_state_widget)
        self.stacked_widget.addWidget(self.results_widget)
        self.stacked_widget.setCurrentWidget(self.empty_state_widget)


        # --- Add all widgets to main layout ---
        self.layout.addLayout(header_layout)
        self.layout.addWidget(url_frame)
        self.layout.addWidget(self.progress_bar)
        self.layout.addWidget(self.stacked_widget, 1) # Make it stretch


    def create_empty_state_widget(self):
        self.empty_state_widget = QWidget()
        layout = QVBoxLayout(self.empty_state_widget)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)

        icon_label = QLabel()
        icon_label.setPixmap(QIcon.fromTheme("text-html").pixmap(128, 128))
        
        message_label = QLabel("Enter a URL to start extracting and summarizing content.")
        message_label.setStyleSheet("font-size: 18px; color: #9e9e9e;")

        layout.addWidget(icon_label, alignment=Qt.AlignCenter)
        layout.addWidget(message_label, alignment=Qt.AlignCenter)

    def create_results_widget(self):
        self.results_widget = QWidget()
        layout = QHBoxLayout(self.results_widget)
        layout.setContentsMargins(0,0,0,0)

        splitter = QSplitter(Qt.Horizontal)
        splitter.setHandleWidth(4)

        # Raw content section
        raw_content_frame = QFrame()
        raw_content_frame.setStyleSheet("background-color: #2d2d2d; border-radius: 8px;")
        raw_content_layout = QVBoxLayout(raw_content_frame)
        
        raw_title_layout = QHBoxLayout()
        raw_icon_label = QLabel()
        raw_icon_label.setPixmap(QIcon.fromTheme("view-list-text", QIcon.fromTheme("document-open")).pixmap(22,22))
        raw_title_layout.addWidget(raw_icon_label)
        raw_title_layout.addWidget(SectionLabel("Raw Content"))
        raw_title_layout.addStretch()

        self.raw_content_text = ThemedTextEdit()
        self.raw_content_text.setReadOnly(True)
        raw_content_layout.addLayout(raw_title_layout)
        raw_content_layout.addWidget(self.raw_content_text)

        # Summary section
        summary_frame = QFrame()
        summary_frame.setStyleSheet("background-color: #2d2d2d; border-radius: 8px;")
        summary_layout = QVBoxLayout(summary_frame)

        summary_title_layout = QHBoxLayout()
        summary_icon_label = QLabel()
        summary_icon_label.setPixmap(QIcon.fromTheme("document-properties", QIcon.fromTheme("document-edit")).pixmap(22,22))
        summary_title_layout.addWidget(summary_icon_label)
        summary_title_layout.addWidget(SectionLabel("Summary"))
        
        # Add download button
        self.download_button = ThemedButton("Download Markdown")
        self.download_button.setIcon(QIcon.fromTheme("document-save"))
        self.download_button.clicked.connect(self.download_summary)
        summary_title_layout.addWidget(self.download_button)
        
        summary_title_layout.addStretch()

        self.summary_text = ThemedTextEdit()
        self.summary_text.setReadOnly(True)
        self.summary_text.setMarkdown("") # To render markdown if needed

        summary_layout.addLayout(summary_title_layout)
        summary_layout.addWidget(self.summary_text)

        splitter.addWidget(raw_content_frame)
        splitter.addWidget(summary_frame)
        splitter.setSizes([600, 600])

        layout.addWidget(splitter)


    def start_processing(self):
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Input Error", "Please enter a URL to process.")
            return

        # --- Start loading state ---
        self.load_button.setText("Loading...")
        self.load_button.setEnabled(False)
        self.url_input.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.raw_content_text.clear()
        self.summary_text.clear()

        # --- Create and start processing thread ---
        self.thread = ProcessingThread(url)
        self.thread.finished.connect(self.on_processing_finished)
        self.thread.start()

    def on_processing_finished(self, raw_content, summary, error_message):
        # --- Stop loading state ---
        self.load_button.setText("Summarize")
        self.load_button.setEnabled(True)
        self.url_input.setEnabled(True)
        self.progress_bar.setVisible(False)

        if error_message:
            QMessageBox.critical(self, "Processing Error", f"An error occurred:\n{error_message}")
            self.stacked_widget.setCurrentWidget(self.empty_state_widget)
        else:
            self.raw_content_text.setText(raw_content)
            self.summary_text.setMarkdown(summary)
            self.stacked_widget.setCurrentWidget(self.results_widget)

    def download_summary(self):
        if not self.summary_text.toPlainText():
            QMessageBox.warning(self, "Download Error", "No summary available to download.")
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Summary as Markdown",
            "",
            "Markdown Files (*.md);;All Files (*.*)"
        )
        
        if file_path:
            try:
                # Get the actual Markdown content from the text edit
                markdown_content = self.summary_text.toMarkdown()
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(markdown_content)
                QMessageBox.information(self, "Success", "Summary saved successfully as Markdown!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save file: {str(e)}")


def main():
    app = QApplication(sys.argv)
    
    # Use a modern, clean font if available
    font = QFont("Segoe UI")  # Changed from Inter to Segoe UI
    font.setPointSize(10)
    app.setFont(font)
    
    # Set custom button style for QMessageBox
    app.setStyleSheet("""
        QMessageBox QPushButton {
            background-color: #009688; color: white; border: none;
            padding: 8px 20px; border-radius: 6px; font-size: 14px;
            font-weight: bold; min-width: 80px;
        }
        QMessageBox QPushButton:hover { background-color: #00a99d; }
        QMessageBox QPushButton:pressed { background-color: #00796b; }
    """)

    window = WebsiteSummarizer()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()