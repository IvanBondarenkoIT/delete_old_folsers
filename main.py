import os
import shutil
from datetime import datetime, timedelta
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFileDialog, QTextEdit


class FolderDeletionApp(QWidget):
    def __init__(self):
        super().__init__()

        # Set default date to current date minus one month
        default_date = datetime.now() - timedelta(days=30)
        self.chosen_date_str = default_date.strftime('%Y-%m-%d')

        self.create_widgets()

    def create_widgets(self):
        self.folder_label = QLabel('Choose Folder:')
        self.folder_entry = QLineEdit()
        self.browse_button = QPushButton('Browse')
        self.browse_button.clicked.connect(self.browse_folder)

        self.date_label = QLabel('Choose Date (YYYY-MM-DD):')
        self.date_entry = QLineEdit(self.chosen_date_str)

        # Date buttons
        self.minus_one_day_button = QPushButton('-1 Day')
        self.minus_one_day_button.clicked.connect(lambda: self.adjust_date(-1))
        self.plus_one_day_button = QPushButton('+1 Day')
        self.plus_one_day_button.clicked.connect(lambda: self.adjust_date(1))
        self.minus_one_month_button = QPushButton('-1 Month')
        self.minus_one_month_button.clicked.connect(lambda: self.adjust_date(-30))
        self.plus_one_month_button = QPushButton('+1 Month')
        self.plus_one_month_button.clicked.connect(lambda: self.adjust_date(30))

        self.run_script_button = QPushButton('Run Script')
        self.run_script_button.clicked.connect(self.run_script)

        self.result_text = QTextEdit()

        layout = QVBoxLayout()
        layout.addWidget(self.folder_label)
        layout.addWidget(self.folder_entry)
        layout.addWidget(self.browse_button)
        layout.addWidget(self.date_label)
        layout.addWidget(self.date_entry)
        layout.addWidget(self.minus_one_day_button)
        layout.addWidget(self.plus_one_day_button)
        layout.addWidget(self.minus_one_month_button)
        layout.addWidget(self.plus_one_month_button)
        layout.addWidget(self.run_script_button)
        layout.addWidget(self.result_text)

        self.setLayout(layout)
        self.setWindowTitle('Folder Deletion Script')

    def browse_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'Choose Folder')
        self.folder_entry.setText(folder_path)

    def adjust_date(self, days):
        current_date = datetime.strptime(self.chosen_date_str, '%Y-%m-%d')
        new_date = current_date + timedelta(days=days)
        self.chosen_date_str = new_date.strftime('%Y-%m-%d')
        self.date_entry.setText(self.chosen_date_str)

    def run_script(self):
        chosen_date_str = self.date_entry.text()
        chosen_date = datetime.strptime(chosen_date_str, '%Y-%m-%d')

        folder_path = self.folder_entry.text()

        if not os.path.exists(folder_path):
            self.result_text.append(f"Invalid folder path: {folder_path}")
            return

        self.result_text.clear()
        self.result_text.append(f"Running script for folder: {folder_path}")
        self.result_text.append(f"Checking folders created before: {chosen_date}\n")

        self.delete_folders_old_than(folder_path, chosen_date)

    def delete_folders_old_than(self, folder_path, chosen_date):
        for root, dirs, files in os.walk(folder_path):
            for folder_name in dirs:
                folder_path = os.path.join(root, folder_name)
                readme_path = os.path.join(folder_path, 'readme.txt')

                if os.path.exists(readme_path):
                    creation_time = os.path.getctime(readme_path)
                    creation_date = datetime.fromtimestamp(creation_time)

                    if creation_date < chosen_date:
                        self.result_text.append(f"Deleting folder: {folder_path}")
                        shutil.rmtree(folder_path)
                    else:
                        self.result_text.append(f"Skipping folder: {folder_path} (created on {creation_date})")
        self.result_text.append("Process completed!")


if __name__ == '__main__':
    app = QApplication([])
    window = FolderDeletionApp()
    window.show()
    app.exec_()
