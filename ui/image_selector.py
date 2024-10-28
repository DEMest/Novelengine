import os
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QListWidget, QHBoxLayout, QSplitter, QSlider
from PyQt5.QtGui import QColor, QPalette, QIcon
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from config.config_manager import save_config
from utils.image_processor import display_image, clear_image

class ImageSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.media_player = QMediaPlayer()
        self.initUI()
        self.selected_image_path = None

    def initUI(self):
        self.setWindowState(Qt.WindowMaximized)
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

        self.audio_button = QPushButton('Показать аудиофайлы', self)
        self.audio_button.setStyleSheet(
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
        self.audio_button.clicked.connect(self.show_audio_files)
        self.toolbox_layout.addWidget(self.audio_button)
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
            "QScrollBar:vertical, QScrollBar:horizontal {"
            "    background: #333333;"
            "    width: 8px;"
            "    height: 8px;"
            "}"
            "QScrollBar::handle:vertical, QScrollBar::handle:horizontal {"
            "    background: #4a4a4a;"
            "    min-height: 20px;"
            "    border-radius: 0px;"
            "}"
            "QScrollBar::handle:vertical:hover, QScrollBar::handle:horizontal:hover {"
            "    background: #5a5a5a;"
            "}"
            "QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical, QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {"
            "    height: 0px;"
            "    width: 0px;"
            "}"
            "QScrollBar::groove:horizontal, QScrollBar::groove:vertical {"
            "    background: #333333;"
            "    border: none;"
            "}"
            "QScrollBar::sub-page:horizontal, QScrollBar::sub-page:vertical {"
            "    background: #333333;"
            "}"
            "QScrollBar::add-page:horizontal, QScrollBar::add-page:vertical {"
            "    background: #2a2a2a;"
            "}"
        )
        self.image_list.itemClicked.connect(self.select_file)

        self.play_button = QPushButton('Воспроизвести', self)
        self.play_button.setStyleSheet(
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
        self.play_button.clicked.connect(self.play_audio)
        self.toolbox_layout.addWidget(self.play_button)

        self.stop_button = QPushButton('Остановить', self)
        self.stop_button.setStyleSheet(
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
        self.stop_button.clicked.connect(self.stop_audio)
        self.toolbox_layout.addWidget(self.stop_button)

        self.position_slider = QSlider(Qt.Horizontal, self)
        self.position_slider.setStyleSheet(
            "QSlider::groove:horizontal {"
            "    background: #2a2a2a;"
            "    height: 8px;"
            "    border-radius: 4px;"
            "}"
            "QSlider::handle:horizontal {"
            "    background: #4a4a4a;"
            "    width: 8px;"
            "    margin: -5px 0;"
            "    border-radius: 2px;"
            "}"
        )
        self.position_slider.sliderMoved.connect(self.set_position)
        self.toolbox_layout.addWidget(self.position_slider)

        toolbox_widget = QWidget()
        toolbox_widget.setLayout(self.toolbox_layout)

        splitter.addWidget(toolbox_widget)
        splitter.addWidget(self.image_list)
        splitter.setStretchFactor(1, 4)
        splitter.setChildrenCollapsible(False)

        main_layout.addWidget(splitter)
        self.setLayout(main_layout)

        self.media_player.positionChanged.connect(self.position_changed)
        self.media_player.durationChanged.connect(self.duration_changed)

    def show_images(self):
        images_path = os.path.join(os.getcwd(), 'assets', 'images')
        self.image_list.clear()
        if os.path.exists(images_path):
            for file_name in os.listdir(images_path):
                if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                    self.image_list.addItem(file_name)

    def show_audio_files(self):
        audio_path = os.path.join(os.getcwd(), 'assets', 'sound')
        self.image_list.clear()
        if os.path.exists(audio_path):
            for file_name in os.listdir(audio_path):
                if file_name.lower().endswith(('.wav', '.mp3', '.aac', '.flac')):
                    self.image_list.addItem(file_name)

    def select_file(self, item):
        selected_path = item.text()
        if selected_path.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            images_path = os.path.join(os.getcwd(), 'assets', 'images')
            self.selected_image_path = os.path.join(images_path, selected_path)
            save_config(self.selected_image_path)
            clear_image(self)
            display_image(self.selected_image_path, self)
        elif selected_path.lower().endswith(('.wav', '.mp3', '.aac', '.flac')):
            audio_path = os.path.join(os.getcwd(), 'assets', 'sound')
            audio_file_path = os.path.join(audio_path, selected_path)
            self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(audio_file_path)))

    def play_audio(self):
        if self.media_player.media() is not None:
            self.media_player.play()

    def stop_audio(self):
        if self.media_player.media() is not None:
            self.media_player.pause()

    def set_position(self, position):
        self.media_player.setPosition(position)

    def position_changed(self, position):
        self.position_slider.setValue(position)

    def duration_changed(self, duration):
        self.position_slider.setRange(0, duration)
