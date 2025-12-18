from PySide6.QtWidgets import QHBoxLayout

from app.view.LeftMenu import LeftMenu
from app.view.RightMenu import RightMenu

class MainApp(QHBoxLayout):
    def __init__(self):
        super().__init__()
        self.setSpacing(0)

        layout_right = RightMenu()
        layout_left = LeftMenu(layout_right)

        self.addLayout(layout_left, 1)
        self.addWidget(layout_right, 4)
