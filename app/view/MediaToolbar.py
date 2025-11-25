from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QToolBar, QPushButton, QSlider, QLabel


assets_path = 'app/assets'

class ClickableSlider(QSlider):
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            x = event.position().x()
            value = self.minimum() + (self.maximum() - self.minimum()) * x / self.width()
            self.setValue(int(value))
            event.accept()
        super().mousePressEvent(event)

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

        self.btn_next = QPushButton()
        self.btn_next.setIcon(QIcon(f'{assets_path}/icons/next.png'))
        self.btn_next.setToolTip("Next")

        self.slider = ClickableSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(10000)
        self.slider.setPageStep(1)
        self.slider.setValue(0)
        self.slider.setTickInterval(1)
        self.slider.setTracking(False)
        self.slider.setToolTip("Progress")

        self.btn_next.setObjectName("media_toolbar_btn")
        self.btn_play.setObjectName("media_toolbar_play")
        self.btn_prev.setObjectName("media_toolbar_prev")

        self.addWidget(self.btn_prev)
        self.addWidget(self.btn_play)
        self.addWidget(self.btn_next)
        self.addWidget(self.slider)

        if controller is not None:
            controller.set_song_slider(self.slider)
            self.btn_play.clicked.connect(lambda: controller.toggle_play(self.btn_play))
            self.btn_next.clicked.connect(controller.next_song)
            self.btn_prev.clicked.connect(controller.prev_song)

            self.slider.valueChanged.connect(lambda: controller.seek_by_percent(self.slider.value() / self.slider.maximum()))



