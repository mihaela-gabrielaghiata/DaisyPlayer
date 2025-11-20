from PySide6.QtCore import QSize
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QToolBar


assets_path = 'app/assets'

class MediaToolbar(QToolBar):
    def __init__(self):
        super().__init__()
        self.setIconSize(QSize(48,48))

        action_prev = QAction(QIcon(f'{assets_path}/icons/back.png'), 'Previous', self)
        action_play = QAction(QIcon(f'{assets_path}/icons/play.png'), 'Play', self)
        action_pause = QAction(QIcon(f'{assets_path}/icons/pause.png'), 'Pause', self)
        action_next = QAction(QIcon(f'{assets_path}/icons/next.png'), 'Next', self)

        self.addAction(action_prev)
        self.addAction(action_play)
        self.addAction(action_pause)
        self.addAction(action_next)



