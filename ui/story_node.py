import os
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsTextItem, QGraphicsScene, QGraphicsPathItem, QMenu, QAction, \
    QTextEdit, QVBoxLayout, QPushButton, QWidget, QMessageBox, QListWidget, QLabel, QGraphicsLineItem
from PyQt5.QtGui import QPen, QBrush, QColor, QPainterPath, QPixmap
from PyQt5.QtCore import Qt, QLineF, QPointF

class StoryNode(QGraphicsPathItem):
    def __init__(self, x, y, width, height, text, file_path, image_path=None, parent=None):
        super().__init__(parent)

        self.file_path = file_path
        self.image_path = image_path
        self.parent = parent  # Сохраняем родителя для отображения изображения в правильной области
        self.connected_nodes = []  # Список связанных узлов
        self.connection_lines = []  # Линии связей для отрисовки
        path = QPainterPath()
        path.addRoundedRect(-width / 2, -height / 2, width, height, 15, 15)
        self.setPath(path)

        self.setBrush(QBrush(QColor(60, 63, 65)))
        self.setPen(QPen(QColor(50, 50, 50), 2))
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)

        # Используем весь текст для создания текстового элемента
        self.text_item = QGraphicsTextItem(text, self)
        self.text_item.setDefaultTextColor(Qt.white)
        self.text_item.setTextWidth(width - 10)  # Ограничиваем текст шириной ноды

        # Центрируем текст в ноде
        text_rect = self.text_item.boundingRect()
        self.text_item.setPos(-text_rect.width() / 2, -text_rect.height() / 2)

        self.preview_image_item = None  # QLabel для отображения изображения при выборе узла

    def contextMenuEvent(self, event):
        menu = QMenu()
        edit_action = QAction("Изменить текст", menu)
        delete_action = QAction("Удалить ноду", menu)
        change_image_action = QAction("Изменить изображение", menu)
        connect_node_action = QAction("Связать с узлом", menu)

        edit_action.triggered.connect(self.edit_text)
        delete_action.triggered.connect(self.delete_node)
        change_image_action.triggered.connect(self.change_image)
        connect_node_action.triggered.connect(self.connect_to_node)

        menu.addAction(edit_action)
        menu.addAction(delete_action)
        menu.addAction(change_image_action)
        menu.addAction(connect_node_action)

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
        if len(new_text.split('\n', 1)[0]) > 12:
            QMessageBox.warning(self.text_edit_widget, "Ошибка", "Первая строка текста должна содержать не более 12 символов.")
            return
        with open(self.file_path, 'w', encoding='utf-8') as file:
            file.write(new_text)

        first_line = new_text.split('\n', 1)[0]
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
            for line, _ in self.connection_lines:
                scene.removeItem(line)
            scene.removeItem(self)

    def change_image(self):
        self.image_select_widget = QWidget()
        self.image_select_widget.setWindowTitle("Выбор изображения для узла")
        layout = QVBoxLayout()

        self.image_list = QListWidget()
        images_path = os.path.join(os.getcwd(), 'assets', 'images')
        if os.path.exists(images_path):
            for file_name in os.listdir(images_path):
                if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp')):
                    self.image_list.addItem(file_name)

        select_button = QPushButton("Выбрать изображение")
        select_button.clicked.connect(self.set_image)

        layout.addWidget(self.image_list)
        layout.addWidget(select_button)
        self.image_select_widget.setLayout(layout)
        self.image_select_widget.show()

    def set_image(self):
        selected_item = self.image_list.currentItem()
        if selected_item:
            image_name = selected_item.text()
            images_path = os.path.join(os.getcwd(), 'assets', 'images')
            self.image_path = os.path.join(images_path, image_name)
            self.image_select_widget.close()

            if self.parent:
                self.show_image()

    def show_image(self):
        if self.image_path and self.parent:
            if not self.preview_image_item:
                self.preview_image_item = QLabel(self.parent)
            self.preview_image_item.setPixmap(QPixmap(self.image_path).scaled(200, 200, Qt.KeepAspectRatio))
            self.preview_image_item.setGeometry(10, self.parent.height() - 220, 200, 200)  # Размещаем изображение в нижнем левом окне
            self.preview_image_item.show()

    def connect_to_node(self):
        self.connect_widget = QWidget()
        self.connect_widget.setWindowTitle("Связать с узлом")
        layout = QVBoxLayout()

        self.node_list = QListWidget()
        scene = self.scene()
        if scene:
            for item in scene.items():
                if isinstance(item, StoryNode) and item != self and item not in self.connected_nodes:
                    self.node_list.addItem(item.text_item.toPlainText())

        connect_button = QPushButton("Связать")
        connect_button.clicked.connect(self.create_connection)

        layout.addWidget(self.node_list)
        layout.addWidget(connect_button)
        self.connect_widget.setLayout(layout)
        self.connect_widget.show()

    def create_connection(self):
        selected_item_text = self.node_list.currentItem()
        if selected_item_text:
            scene = self.scene()
            if scene:
                for item in scene.items():
                    if isinstance(item, StoryNode) and item.text_item.toPlainText() == selected_item_text.text():
                        # Проверяем, есть ли уже связь в любую сторону
                        if item in self.connected_nodes or self in item.connected_nodes:
                            QMessageBox.warning(self.connect_widget, "Ошибка", "Эти узлы уже связаны.")
                            return
                        self.connected_nodes.append(item)
                        self.draw_connection(item)
        self.connect_widget.close()

    def draw_connection(self, target_node):
        line = QGraphicsLineItem()
        line.setPen(QPen(Qt.white, 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        self.update_connection_line(line, target_node)
        self.connection_lines.append((line, target_node))
        target_node.connection_lines.append((line, self))
        self.scene().addItem(line)

    def update_connection_line(self, line, target_node):
        start_point = self.get_edge_point(target_node.scenePos())
        end_point = target_node.get_edge_point(self.scenePos())
        line.setLine(QLineF(start_point, end_point))

    def get_edge_point(self, target_pos):
        rect = self.mapRectToScene(self.boundingRect())
        center = rect.center()
        direction = target_pos - center
        if abs(direction.x()) > abs(direction.y()):
            # Линия пересекает левую или правую сторону
            if direction.x() > 0:
                edge_x = rect.right()
            else:
                edge_x = rect.left()
            edge_y = center.y() + direction.y() * (edge_x - center.x()) / direction.x()
        else:
            # Линия пересекает верхнюю или нижнюю сторону
            if direction.y() > 0:
                edge_y = rect.bottom()
            else:
                edge_y = rect.top()
            edge_x = center.x() + direction.x() * (edge_y - center.y()) / direction.y()
        return QPointF(edge_x, edge_y)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            new_pos = value
            for line, target_node in self.connection_lines:
                if isinstance(line, QGraphicsLineItem):
                    self.update_connection_line(line, target_node)
            return new_pos
        return super().itemChange(change, value)

class StoryScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.load_existing_nodes()

    def add_story_node(self, x, y, width=100, height=60, text="Новый узел", image_path=None):
        text_path = os.path.join(os.getcwd(), 'assets', 'text')
        if not os.path.exists(text_path):
            os.makedirs(text_path)

        first_line = text.split('\n')[0]
        if len(first_line) > 12:
            QMessageBox.warning(None, "Ошибка", "Первая строка текста должна содержать не более 12 символов.")
            return

        file_name = f"{first_line}.txt"
        file_path = os.path.join(text_path, file_name)

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(text)
        print(f"[Отладка] Создали файл: {file_path}")

        new_node = StoryNode(0, 0, width, height, text, file_path, image_path, parent=self.parent)
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
                            parent = self.parent if self.parent else None
                            new_node = StoryNode(x, y, 100, 60, node_text, file_path, parent=parent)
                            self.addItem(new_node)
                            self.update()

    def mousePressEvent(self, event):
        item = self.itemAt(event.scenePos(), self.views()[0].transform())
        if isinstance(item, StoryNode):
            item.show_image()
        super().mousePressEvent(event)
