import os
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QListWidget, QHBoxLayout, QSplitter
from PyQt5.QtGui import QColor, QPalette, QIcon
from PyQt5.QtCore import Qt
from config.config_manager import save_config
from utils.image_processor import display_image, clear_image

class ImageSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.selected_image_path = None

    def initUI(self):
        self.setGeometry(100, 100, 1000, 700)
        self.setWindowTitle('Выбор фона')

        icon_path = os.path.join(os.getcwd(), 'assets', 'icons', 'app_icon.png')
        self.setWindowIcon(QIcon(icon_path))

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        self.setPalette(palette)

        main_layout = QHBoxLayout(self)
        splitter = QSplitter(Qt.Horizontal)

        self.toolbox_layout = QVBoxLayout()
        self.select_button = QPushButton('Показать изображения', self)
        self.select_button.setStyleSheet(
            "QPushButton {"
            "    background-color: #2a2a2a;"
            "    color: white;"
            "    font-weight: bold;"
            "    padding: 10px;"
            "    border-radius: 5px;"
            "}"
            "QPushButton:hover {"
            "    background-color: #3a3a3a;"
            "}"
            "QPushButton:pressed {"
            "    background-color: #1a1a1a;"
            "}"
        )
        self.select_button.clicked.connect(self.show_images)
        self.toolbox_layout.addWidget(self.select_button)
        self.toolbox_layout.addStretch()

        self.image_list = QListWidget(self)
        self.image_list.setStyleSheet(
            "QListWidget {"
            "    background-color: #2a2a2a;"
            "    color: white;"
            "    padding: 5px;"
            "    font-size: 12px;"
            "    border: none;"
            "}"
            "QListWidget::item {"
            "    padding: 5px;"
            "}"
            "QListWidget::item:selected {"
            "    background-color: #3a3a3a;"
            "    outline: none;"
            "}"
            "QScrollBar:vertical {"
            "    background: transparent;"
            "    width: 8px;"
            "}"
            "QScrollBar::handle:vertical {"
            "    background: #3a3a3a;"
            "    min-height: 20px;"
            "    border-radius: 0px;"
            "}"
            "QScrollBar::handle:vertical:hover {"
            "    background: #5a5a5a;"
            "}"
            "QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {"
            "    height: 0px;"
            "}"
        )
        self.image_list.itemClicked.connect(self.select_image)

        toolbox_widget = QWidget()
        toolbox_widget.setLayout(self.toolbox_layout)

        splitter.addWidget(toolbox_widget)
        splitter.addWidget(self.image_list)
        splitter.setStretchFactor(1, 4)
        splitter.setChildrenCollapsible(False)  # Отключаем сворачивание справа

        main_layout.addWidget(splitter)
        self.setLayout(main_layout)

    def show_images(self):
        images_path = os.path.join(os.getcwd(), 'assets', 'images')
        self.image_list.clear()
        if os.path.exists(images_path):
            for file_name in os.listdir(images_path):
                if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                    self.image_list.addItem(file_name)

    def select_image(self, item):
        images_path = os.path.join(os.getcwd(), 'assets', 'images')
        self.selected_image_path = os.path.join(images_path, item.text())
        save_config(self.selected_image_path)
        clear_image(self)
        display_image(self.selected_image_path, self)
