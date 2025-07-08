import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication, QVBoxLayout, QLineEdit, QPushButton, QMessageBox
)
from frameless_window import FramelessWindow  # 你封装的窗口类


class LoginWindow(FramelessWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("登录")
        self.resize(400, 280)
        self.setMinimumSize(300, 250)
        self.title_label.setText("  登录系统  ")

        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(60, 40, 60, 40)  # 让内容稍微居中点

        # 用户名输入，默认值admin
        self.username_input = QLineEdit()
        self.username_input.setText("admin")
        self.username_input.setFixedHeight(36)
        self.username_input.setPlaceholderText("请输入用户名")
        self.username_input.setStyleSheet(self._input_style())

        # 密码输入，默认值123456
        self.password_input = QLineEdit()
        self.password_input.setText("123456")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedHeight(36)
        self.password_input.setPlaceholderText("请输入密码")
        self.password_input.setStyleSheet(self._input_style())

        # 登录按钮，浅绿色
        self.login_btn = QPushButton("登录")
        self.login_btn.setCursor(Qt.PointingHandCursor)
        self.login_btn.setFixedHeight(36)
        self.login_btn.setStyleSheet("""
            QPushButton {
                background-color: #a6d785;
                color: #2d4a11;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #8ec354;
            }
        """)
        self.login_btn.clicked.connect(self.handle_login)

        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_btn)

        self.setContentLayout(layout)

    def _input_style(self):
        return """
            QLineEdit {
                border: 1px solid #bbb;
                border-radius: 6px;
                padding: 0 10px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #8ec354;
            }
        """

    def handle_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if username == "admin" and password == "123456":
            QMessageBox.information(self, "登录成功", "欢迎回来！")
        else:
            QMessageBox.warning(self, "登录失败", "用户名或密码错误！")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = LoginWindow()
    win.show()
    sys.exit(app.exec())
