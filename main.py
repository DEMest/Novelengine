import sys
from PyQt5.QtWidgets import QApplication
from ui.image_selector import ImageSelector
from config.config_manager import load_config
from utils.image_processor import display_image, clear_image

if __name__ == "__main__":
    app = QApplication(sys.argv)
    selector = ImageSelector()

    selected_image_path = load_config()
    if selected_image_path:
        display_image(selected_image_path, selector)

    selector.show()
    sys.exit(app.exec_())