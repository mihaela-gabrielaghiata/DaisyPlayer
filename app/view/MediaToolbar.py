from PySide6.QtCore import QSize
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QToolBar, QPushButton

assets_path = 'app/assets'

class MediaToolbar(QToolBar):
    def __init__(self):
        super().__init__()
        self.setIconSize(QSize(48,48))

        btn_prev = QPushButton()
        btn_prev.setIcon(QIcon(f'{assets_path}/icons/back.png'))
        btn_prev.setToolTip("Previous")

        btn_play = QPushButton()
        btn_play.setIcon(QIcon(f'{assets_path}/icons/play.png'))
        btn_play.setToolTip("Play")

        btn_pause = QPushButton()
        btn_pause.setIcon(QIcon(f'{assets_path}/icons/pause.png'))
        btn_pause.setToolTip("Pause")

        btn_next = QPushButton()
        btn_next.setIcon(QIcon(f'{assets_path}/icons/next.png'))
        btn_next.setToolTip("Next")

        btn_next.setObjectName("media_toolbar_btn")
        btn_play.setObjectName("media_toolbar_play")
        btn_pause.setObjectName("media_toolbar_pause")
        btn_prev.setObjectName("media_toolbar_prev")

        self.addWidget(btn_prev)
        self.addWidget(btn_play)
        self.addWidget(btn_pause)
        self.addWidget(btn_next)


