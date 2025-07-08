import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout

from MacWindow import MacWindow


class MyApp(MacWindow):
    def __init__(self):
        super().__init__(title="仿 Mac 无边框窗口", min_size=(500, 400), default_size=(700, 500))

        layout = QVBoxLayout()
        label = QLabel("🍎 这里是仿 Mac 的窗口框架！")
        label.setMouseTracking(True)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        self.setContentLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())
