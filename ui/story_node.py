import os
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsTextItem, QGraphicsScene, QGraphicsPathItem, QMenu, QAction, \
    QTextEdit, QVBoxLayout, QPushButton, QWidget, QFileDialog, QMessageBox
from PyQt5.QtGui import QPen, QBrush, QColor, QPainterPath, QPixmap
from PyQt5.QtCore import Qt
import string

class StoryNode(QGraphicsPathItem):
    def __init__(self, x, y, width, height, text, file_path, image_path=None, parent=None):
        super().__init__(parent)

        self.file_path = file_path
        self.image_path = image_path
        path = QPainterPath()
        path.addRoundedRect(-width / 2, -height / 2, width, height, 15, 15)
        self.setPath(path)

        self.setBrush(QBrush(QColor(60, 63, 65)))
        self.setPen(QPen(QColor(50, 50, 50), 2))
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)

        self.text_item = QGraphicsTextItem(text, self)
        self.text_item.setDefaultTextColor(Qt.white)
        self.text_item.setPos(-width / 4, -height / 4)

        if self.image_path:
            pixmap = QPixmap(self.image_path).scaled(width / 2, height / 2, Qt.KeepAspectRatio)
            self.image_item = QGraphicsTextItem(self)
            self.image_item.setPixmap(pixmap)
            self.image_item.setPos(-width / 2, -height / 2 - pixmap.height())

    def contextMenuEvent(self, event):
        menu = QMenu()
        edit_action = QAction("Изменить текст", menu)
        delete_action = QAction("Удалить ноду", menu)
        change_image_action = QAction("Изменить изображение", menu)

        edit_action.triggered.connect(lambda: self.edit_text())
        delete_action.triggered.connect(lambda: self.delete_node())
        change_image_action.triggered.connect(lambda: self.change_image())

        menu.addAction(edit_action)
        menu.addAction(delete_action)
        menu.addAction(change_image_action)

        menu.exec_(event.screenPos())

    def edit_text(self):
        self.text_edit_widget = QWidget()
        self.text_edit_widget.setWindowTitle("Редактирование текста узла")
        layout = QVBoxLayout()
        self.text_edit = QTextEdit()
        with open(self.file_path, 'r', encoding='utf-8') as file:
            self.text_edit.setText(file.read())

        save_button = QPushButton("Сохранить")
        save_button.clicked.connect(self.save_text)

        layout.addWidget(self.text_edit)
        layout.addWidget(save_button)
        self.text_edit_widget.setLayout(layout)
        self.text_edit_widget.show()

    def save_text(self):
        new_text = self.text_edit.toPlainText()
        with open(self.file_path, 'w', encoding='utf-8') as file:
            file.write(new_text)

        first_line = new_text.split('\n')[0]
        self.text_item.setPlainText(first_line)
        self.text_edit_widget.close()

        new_file_name = f"{first_line}.txt"
        new_file_path = os.path.join(os.path.dirname(self.file_path), new_file_name)
        if new_file_path != self.file_path:
            os.rename(self.file_path, new_file_path)
            self.file_path = new_file_path

    def delete_node(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
        scene = self.scene()
        if scene:
            scene.removeItem(self)

    def change_image(self):
        image_path, _ = QFileDialog.getOpenFileName(None, "Выберите изображение", "",
                                                    "Images (*.png *.jpg *.jpeg *.bmp *.gif)")
        if image_path:
            self.image_path = image_path
            if hasattr(self, 'image_item'):
                self.image_item.setPixmap(QPixmap(self.image_path).scaled(50, 50, Qt.KeepAspectRatio))
            else:
                pixmap = QPixmap(self.image_path).scaled(50, 50, Qt.KeepAspectRatio)
                self.image_item = QGraphicsTextItem(self)
                self.image_item.setPixmap(pixmap)
                self.image_item.setPos(-50, -50)


class StoryScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.load_existing_nodes()

    def add_story_node(self, x, y, width=100, height=60, text="Новый узел", image_path=None):
        text_path = os.path.join(os.getcwd(), 'assets', 'text')
        if not os.path.exists(text_path):
            os.makedirs(text_path)

        first_line = text.split('\n')[0]
        file_name = f"{first_line}.txt"
        file_path = os.path.join(text_path, file_name)

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(text)
        print(f"[Отладка] Создали файл: {file_path}")

        new_node = StoryNode(0, 0, width, height, first_line, file_path, image_path)
        self.addItem(new_node)
        new_node.setPos(x, y)
        self.update()
        print(f"[Отладка] Создали и добавили узел: {first_line} на позиции ({x}, {y})")

        if self.views():
            view = self.views()[0]
            view.centerOn(new_node)
            view.viewport().update()
            print(f"[Отладка] Обновили виджет сцены после добавления узла.")

    def load_existing_nodes(self):
        text_path = os.path.join(os.getcwd(), 'assets', 'text')
        if os.path.exists(text_path):
            files = os.listdir(text_path)
            for i, file_name in enumerate(files):
                if file_name.endswith('.txt'):
                    file_path = os.path.join(text_path, file_name)
                    with open(file_path, 'r', encoding='utf-8') as file:
                        lines = file.readlines()
                        if lines:
                            node_text = lines[0].strip()
                            x = (i % 5) * 50  # Позиционирование узлов по сетке
                            y = (i // 5) * 80
                            new_node = StoryNode(x, y, 100, 60, node_text, file_path)
                            self.addItem(new_node)
                            self.update()

    def create_node_link(self, node1, node2):
        pass