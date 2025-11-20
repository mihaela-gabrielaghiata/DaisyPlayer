from PySide6.QtCore import QSize
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QToolBar


assets_path = 'app/assets'

class TopToolbar(QToolBar):
    def __init__(self):
        super().__init__()
        self.setIconSize(QSize(48,48))
        self.addAction(QAction(QIcon(f'{assets_path}/icons/icon.png'),'', self))

