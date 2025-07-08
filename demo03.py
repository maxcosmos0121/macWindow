import sys

from PySide6.QtCore import Qt, QPoint
from PySide6.QtWidgets import (
    QApplication, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
    QListWidget, QListWidgetItem, QLabel, QMenu
)
from frameless_window import FramelessWindow


class CustomLineEdit(QLineEdit):
    def contextMenuEvent(self, event):
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: #fff;
                border: 1px solid #ccc;
                border-radius: 0px;
                padding: 4px 0;
                font-size: 14px;
                color: #333;
            }
            QMenu::item {
                padding: 6px 20px;
            }
            QMenu::item:selected {
                background-color: #4caf50;
                color: white;
            }
        """)
        undo_action = menu.addAction("撤销")
        redo_action = menu.addAction("重做")
        menu.addSeparator()
        cut_action = menu.addAction("剪切")
        copy_action = menu.addAction("复制")
        paste_action = menu.addAction("粘贴")
        select_all_action = menu.addAction("全选")

        undo_action.triggered.connect(self.undo)
        redo_action.triggered.connect(self.redo)
        cut_action.triggered.connect(self.cut)
        copy_action.triggered.connect(self.copy)
        paste_action.triggered.connect(self.paste)
        select_all_action.triggered.connect(self.selectAll)

        menu.exec(event.globalPos())


class TodoApp(FramelessWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("待办事项")
        self.resize(500, 400)
        self.setMinimumSize(400, 300)
        self.title_label.setText("  我的待办事项  ")

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 20)
        layout.setSpacing(15)

        # 输入区
        input_layout = QHBoxLayout()
        self.input_line = CustomLineEdit()
        self.input_line.setPlaceholderText("添加新的待办事项...")
        self.input_line.setStyleSheet(self._input_style())
        self.input_line.setFixedHeight(36)
        self.input_line.returnPressed.connect(self.add_item)

        self.add_btn = QPushButton("添加")
        self.add_btn.setFixedWidth(80)
        self.add_btn.setFixedHeight(36)
        self.add_btn.setCursor(Qt.PointingHandCursor)
        self.add_btn.setStyleSheet(self._button_style())
        self.add_btn.clicked.connect(self.add_item)

        input_layout.addWidget(self.input_line)
        input_layout.addWidget(self.add_btn)

        # 待办事项列表
        self.todo_list = QListWidget()
        self.todo_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.todo_list.customContextMenuRequested.connect(self.show_context_menu)
        self.todo_list.itemClicked.connect(self.toggle_item_done)

        self.todo_list.setStyleSheet("""
            QListWidget {
                border: 0.5px solid #ddd;
                border-radius: 4px;
                padding: 6px;
                font-size: 15px;
                background-color: #fff;
            }
        """)

        # 状态栏
        self.status_label = QLabel("右键点击事项可删除")
        self.status_label.setStyleSheet("color: #666666; font-size: 13px;")

        layout.addLayout(input_layout)
        layout.addWidget(self.todo_list)
        layout.addWidget(self.status_label)

        self.setContentLayout(layout)

    def _input_style(self):
        return """
            QLineEdit {
                border: 0.5px solid #aaa;
                border-radius: 4px;
                padding: 0 12px;
                font-size: 15px;
                color: #333;
                background-color: #fafafa;
            }
            QLineEdit:focus {
                border-color: #4caf50;
                background-color: #fff;
            }
        """

    def _button_style(self):
        return """
            QPushButton {
                background-color: #4caf50;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 15px;
                font-weight: 600;
                padding: 8px 15px;
                transition: background-color 0.2s ease;
            }
            QPushButton:hover {
                background-color: #3a9d3a;
            }
            QPushButton:pressed {
                background-color: #357a34;
            }
        """

    def add_item(self):
        text = self.input_line.text().strip()
        if not text:
            return

        item = QListWidgetItem(text)
        # 初始状态：未完成，黑色字体，无删除线
        self.set_item_done(item, done=False)
        self.todo_list.addItem(item)
        self.input_line.clear()
        self.status_label.setText(f"添加事项：{text}")

    def show_context_menu(self, pos: QPoint):
        item = self.todo_list.itemAt(pos)
        if item:
            menu = QMenu(self)
            menu.setStyleSheet("""
                QMenu {
                    background-color: #fff;
                    border: 1px solid #ccc;
                    border-radius: 0px;
                    padding: 4px 0;
                    font-size: 14px;
                    color: #333;
                }
                QMenu::item {
                    padding: 6px 20px;
                }
                QMenu::item:selected {
                    background-color: #4caf50;
                    color: white;
                }
            """)
            delete_action = menu.addAction("删除该事项")
            action = menu.exec(self.todo_list.mapToGlobal(pos))
            if action == delete_action:
                self.todo_list.takeItem(self.todo_list.row(item))
                self.status_label.setText("已删除一项事项")

    def toggle_item_done(self, item: QListWidgetItem):
        # 切换完成状态
        done = item.data(Qt.UserRole) or False
        self.set_item_done(item, not done)

    def set_item_done(self, item: QListWidgetItem, done: bool):
        """根据完成状态设置字体样式和颜色"""
        font = item.font()
        font.setStrikeOut(done)
        item.setFont(font)
        if done:
            item.setForeground(Qt.gray)
            item.setData(Qt.UserRole, True)
            self.status_label.setText(f"完成事项：{item.text()}")
        else:
            item.setForeground(Qt.black)
            item.setData(Qt.UserRole, False)
            self.status_label.setText(f"未完成事项：{item.text()}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = TodoApp()
    win.show()
    sys.exit(app.exec())
