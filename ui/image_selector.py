import os
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QListWidget, QHBoxLayout, QSplitter, QSlider, QGraphicsView, QGraphicsScene, QMenuBar, QAction, QTextEdit
from PyQt5.QtGui import QColor, QPalette, QIcon, QPixmap, QDrag
from PyQt5.QtCore import Qt, QUrl, QMimeData
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from config.config_manager import save_config
from ui.story_node import StoryScene
from PyQt5.QtGui import QPainter

class ImageSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.media_player = QMediaPlayer()
        self.initUI()
        self.selected_image_path = None
        self.canvas_view = QGraphicsView()
        self.canvas_scene = QGraphicsScene(self)
        self.canvas_view.setScene(self.canvas_scene)
        self.canvas_view.setRenderHint(QPainter.Antialiasing, True)
        self.canvas_view.setAcceptDrops(True)
        self.canvas_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.canvas_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

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
        self.select_button = QPushButton('Изображения', self)
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

        self.audio_button = QPushButton('Аудиофайлы', self)
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

        self.video_button = QPushButton('Видеофайлы', self)
        self.video_button.setStyleSheet(
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
        self.video_button.clicked.connect(self.show_video_files)
        self.toolbox_layout.addWidget(self.video_button)
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
            "    background: #2a2a2a;"  # Меняем на цвет фона списка
            "    width: 10px;"
            "    height: 10px;"
            "}"
            "QScrollBar::handle:vertical, QScrollBar::handle:horizontal {"
            "    background: #4a4a4a;"
            "    min-height: 20px;"
            "    border-radius: 4px;"
            "}"
            "QScrollBar::handle:vertical:hover, QScrollBar::handle:horizontal:hover {"
            "    background: #5a5a5a;"
            "}"
            "QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical, QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {"
            "    background: none;"
            "    height: 0px;"
            "    width: 0px;"
            "}"
            "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical, QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {"
            "    background: none;"
            "}"
            "QScrollBar::groove:horizontal, QScrollBar::groove:vertical {"
            "    background: #2a2a2a;"
            "    border: none;"
            "}"
        )
        self.image_list.itemClicked.connect(self.select_file)
        self.image_list.setDragEnabled(True)

        toolbox_widget = QWidget()
        toolbox_widget.setLayout(self.toolbox_layout)

        self.preview_view = QGraphicsView()
        self.preview_scene = QGraphicsScene()
        self.preview_view.setScene(self.preview_scene)
        self.preview_view.setStyleSheet("background-color: #1a1a1a;")
        self.preview_view.setRenderHint(QPainter.Antialiasing, True)
        self.preview_view.setRenderHint(QPainter.SmoothPixmapTransform, True)
        self.preview_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.preview_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.preview_view.scale(0.8, 0.8)

        self.canvas_view = QGraphicsView()
        self.canvas_scene = QGraphicsScene()
        self.canvas_view.setScene(self.canvas_scene)
        self.canvas_view.setStyleSheet("background-color: #1a1a1a;")
        self.canvas_view.setRenderHint(QPainter.Antialiasing, True)
        self.canvas_view.setRenderHint(QPainter.SmoothPixmapTransform, True)
        self.canvas_view.setAcceptDrops(True)
        self.canvas_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.canvas_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.story_view = QGraphicsView()
        self.story_scene = StoryScene()
        self.story_view.setScene(self.story_scene)
        self.story_view.setStyleSheet("background-color: #1a1a1a;")
        self.story_view.setRenderHint(QPainter.Antialiasing, True)
        self.story_view.setRenderHint(QPainter.SmoothPixmapTransform, True)
        self.story_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.story_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        splitter.addWidget(toolbox_widget)
        splitter.addWidget(self.image_list)

        right_splitter = QSplitter(Qt.Vertical)
        right_splitter.addWidget(self.preview_view)
        right_splitter.addWidget(self.canvas_view)
        right_splitter.setStretchFactor(0, 3)
        right_splitter.setStretchFactor(1, 5)
        right_splitter.setChildrenCollapsible(False)

        splitter.addWidget(right_splitter)
        splitter.addWidget(self.story_view)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 4)
        splitter.setStretchFactor(2, 2)
        splitter.setChildrenCollapsible(False)
        splitter.setSizes([500, 1000, 500])

        main_layout.addWidget(splitter)
        self.setLayout(main_layout)

        self.menu_bar = QMenuBar(self)
        file_menu = self.menu_bar.addMenu('File')
        save_action = QAction('Save Project', self)
        save_action.triggered.connect(self.save_project)
        load_action = QAction('Load Project', self)
        load_action.triggered.connect(self.load_project)
        file_menu.addAction(save_action)
        file_menu.addAction(load_action)

        edit_menu = self.menu_bar.addMenu('Edit')
        undo_action = QAction('Undo', self)
        redo_action = QAction('Redo', self)
        edit_menu.addAction(undo_action)
        edit_menu.addAction(redo_action)

        main_layout.setMenuBar(self.menu_bar)

        self.media_player.positionChanged.connect(self.position_changed)
        self.media_player.durationChanged.connect(self.duration_changed)

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
            "    width: 16px;"
            "    margin: -5px 0;"
            "    border-radius: 4px;"
            "}"
        )
        self.position_slider.sliderMoved.connect(self.set_position)
        self.toolbox_layout.addWidget(self.position_slider)

        self.dialog_text = QTextEdit(self)
        self.dialog_text.setStyleSheet("background-color: #2a2a2a; color: white; padding: 10px; border-radius: 5px;")
        self.toolbox_layout.addWidget(self.dialog_text)

        add_node_button = QPushButton('Добавить узел', self)
        add_node_button.setStyleSheet(
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
        add_node_button.clicked.connect(self.add_story_node)
        self.toolbox_layout.addWidget(add_node_button)

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

    def show_video_files(self):
        video_path = os.path.join(os.getcwd(), 'assets', 'video')
        self.image_list.clear()
        if os.path.exists(video_path):
            for file_name in os.listdir(video_path):
                if file_name.lower().endswith(('.mov', '.mp4', '.avi')):
                    self.image_list.addItem(file_name)

    def select_file(self, item):
        selected_path = item.text()
        if selected_path.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            images_path = os.path.join(os.getcwd(), 'assets', 'images')
            self.selected_image_path = os.path.join(images_path, selected_path)
            pixmap = QPixmap(self.selected_image_path)
            self.preview_scene.clear()
            self.preview_scene.addPixmap(pixmap)
            self.preview_view.fitInView(self.preview_scene.itemsBoundingRect(), Qt.KeepAspectRatio)
        elif selected_path.lower().endswith(('.wav', '.mp3', '.aac', '.flac')):
            audio_path = os.path.join(os.getcwd(), 'assets', 'sound')
            audio_file_path = os.path.join(audio_path, selected_path)
            self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(audio_file_path)))
        elif selected_path.lower().endswith(('.mov', '.mp4', '.avi')):
            video_path = os.path.join(os.getcwd(), 'assets', 'video')
            video_file_path = os.path.join(video_path, selected_path)
            self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(video_file_path)))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            item = self.preview_scene.itemAt(self.preview_view.mapToScene(event.pos()), self.preview_view.transform())
            if item:
                drag = QDrag(self)
                mime_data = QMimeData()
                mime_data.setText(self.selected_image_path)
                drag.setMimeData(mime_data)
                drag.exec_(Qt.CopyAction)

    def dropEvent(self, event):
        if event.mimeData().hasText():
            image_path = event.mimeData().text()
            pixmap = QPixmap(image_path)
            self.canvas_scene.addPixmap(pixmap)
            save_config(image_path)

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

    def wheelEvent(self, event):
        if self.preview_view.hasFocus():
            if event.angleDelta().y() > 0:
                factor = 1.1
            elif event.angleDelta().y() < 0:
                factor = 0.9
            else:
                return
            self.preview_view.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
            self.preview_view.scale(factor, factor)
            self.preview_view.setTransformationAnchor(QGraphicsView.AnchorViewCenter)
        elif self.story_view.hasFocus():
            if event.angleDelta().y() > 0:
                factor = 1.1
            elif event.angleDelta().y() < 0:
                factor = 0.9
            else:
                return
            self.story_view.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
            self.story_view.scale(factor, factor)
            self.story_view.setTransformationAnchor(QGraphicsView.AnchorViewCenter)

    def keyPressEvent(self, event):
        if event.modifiers() == Qt.ShiftModifier:
            if event.key() == Qt.Key_Left:
                self.preview_view.horizontalScrollBar().setValue(self.preview_view.horizontalScrollBar().value() - 20)
            elif event.key() == Qt.Key_Right:
                self.preview_view.horizontalScrollBar().setValue(self.preview_view.horizontalScrollBar().value() + 20)
        elif event.modifiers() == Qt.ControlModifier:
            if event.key() == Qt.Key_Up:
                self.preview_view.verticalScrollBar().setValue(self.preview_view.verticalScrollBar().value() - 20)
            elif event.key() == Qt.Key_Down:
                self.preview_view.verticalScrollBar().setValue(self.preview_view.verticalScrollBar().value() + 20)
        elif event.modifiers() == Qt.AltModifier:
            if event.key() == Qt.Key_Equal:
                self.preview_view.scale(1.1, 1.1)
            elif event.key() == Qt.Key_Minus:
                self.preview_view.scale(0.9, 0.9)

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Alt:
            self.preview_view.setTransformationAnchor(QGraphicsView.AnchorViewCenter)

    def save_project(self):
        save_config('project_state')

    def load_project(self):
        pass

    def add_story_node(self):
        text = self.dialog_text.toPlainText()
        if text:
            node_name = text.split('\n', 1)[0]
            file_path = os.path.join('assets', 'text', f"{node_name}.txt")
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(text)
            current_nodes = len(self.story_scene.items())
            offset = 100 * current_nodes
            self.story_scene.add_story_node(offset, offset, text=node_name)
