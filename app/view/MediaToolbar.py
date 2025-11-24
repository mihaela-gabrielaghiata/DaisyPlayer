from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QToolBar, QPushButton, QSlider, QLabel


assets_path = 'app/assets'

class MediaToolbar(QToolBar):
    def __init__(self, controller=None):
        super().__init__()
        self.setIconSize(QSize(48,48))

        self.btn_prev = QPushButton()
        self.btn_prev.setIcon(QIcon(f'{assets_path}/icons/back.png'))
        self.btn_prev.setToolTip("Previous")

        self.btn_play = QPushButton()
        self.btn_play.setIcon(QIcon(f'{assets_path}/icons/play.png'))
        self.btn_play.setToolTip("Play")

        self.btn_pause = QPushButton()
        self.btn_pause.setIcon(QIcon(f'{assets_path}/icons/pause.png'))
        self.btn_pause.setToolTip("Pause")

        self.btn_next = QPushButton()
        self.btn_next.setIcon(QIcon(f'{assets_path}/icons/next.png'))
        self.btn_next.setToolTip("Next")

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(0)
        self.slider.setToolTip("Progress")

        self.btn_next.setObjectName("media_toolbar_btn")
        self.btn_play.setObjectName("media_toolbar_play")
        self.btn_pause.setObjectName("media_toolbar_pause")
        self.btn_prev.setObjectName("media_toolbar_prev")

        self.addWidget(self.btn_prev)
        self.addWidget(self.btn_play)
        self.addWidget(self.btn_pause)
        self.addWidget(self.btn_next)
        self.addWidget(self.slider)

        if controller is not None:
            self.btn_play.clicked.connect(controller.toggle_play)
            self.btn_pause.clicked.connect(controller.pause)
            self.btn_next.clicked.connect(controller.next_song)
            self.btn_prev.clicked.connect(controller.prev_song)

            self.slider.sliderReleased.connect(lambda: controller.seek_by_percent(self.slider.value()))



