from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

def display_image(image_path, parent_widget):
    image_label = QLabel(parent_widget)
    pixmap = QPixmap(image_path)
    image_label.setPixmap(pixmap.scaled(800, 600, Qt.KeepAspectRatio, Qt.SmoothTransformation))
    image_label.setAlignment(Qt.AlignCenter)
    parent_widget.layout().addWidget(image_label)
    parent_widget.image_label = image_label

def clear_image(parent_widget):
    if hasattr(parent_widget, 'image_label'):
        parent_widget.layout().removeWidget(parent_widget.image_label)
        parent_widget.image_label.deleteLater()
        del parent_widget.image_label