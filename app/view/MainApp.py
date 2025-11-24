from PySide6.QtWidgets import QHBoxLayout

from app.view.LeftMenu import LeftMenu
from app.view.RightMenu import RightMenu

class MainApp(QHBoxLayout):
    def __init__(self):
        super().__init__()
        self.setSpacing(0)

        layout_left = LeftMenu()
        layout_right = RightMenu()

        self.addLayout(layout_left, 1)
        self.addLayout(layout_right, 4)