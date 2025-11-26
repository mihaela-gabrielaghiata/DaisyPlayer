from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QToolBar, QPushButton, QSlider, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QSizePolicy


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

        self.btn_prev = QPushButton()
        self.btn_prev.setIcon(QIcon(f'{assets_path}/icons/back.png'))
        self.btn_prev.setToolTip("Previous")
        self.btn_prev.setIconSize(QSize(38,38))

        self.btn_play = QPushButton()
        self.btn_play.setIcon(QIcon(f'{assets_path}/icons/play.png'))
        self.btn_play.setToolTip("Play")
        self.btn_play.setIconSize(QSize(48,48))

        self.btn_next = QPushButton()
        self.btn_next.setIcon(QIcon(f'{assets_path}/icons/next.png'))
        self.btn_next.setToolTip("Next")
        self.btn_next.setIconSize(QSize(38,38))

        self.slider = ClickableSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(10000)
        self.slider.setPageStep(1)
        self.slider.setValue(0)
        self.slider.setTickInterval(1)
        self.slider.setTracking(False)
        self.slider.setToolTip("Progress")

        self.btn_shuffle = QPushButton()
        self.btn_shuffle.setCheckable(True)
        self.btn_shuffle.setIcon(QIcon(f'{assets_path}/icons/shuffle.png'))
        self.btn_shuffle.setToolTip("Shuffle")
        self.btn_shuffle.setIconSize(QSize(30,30))

        self.btn_repeat = QPushButton()
        self.btn_repeat.setCheckable(True)
        self.btn_repeat.setIcon(QIcon(f'{assets_path}/icons/repeat.png'))
        self.btn_repeat.setToolTip("Repeat")
        self.btn_repeat.setIconSize(QSize(30,30))

        self.slider_volume = ClickableSlider(Qt.Horizontal)
        self.slider_volume.setFixedWidth(150)
        self.slider_volume.setMinimum(0)
        self.slider_volume.setMaximum(100)
        self.slider_volume.setPageStep(1)
        self.slider_volume.setValue(50)
        self.slider_volume.setTickInterval(1)
        self.slider_volume.setTracking(False)
        self.slider_volume.setToolTip("Volume")

        self.music_label = QLabel('')
        self.music_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.music_label.setAlignment(Qt.AlignCenter)

        self.btn_next.setObjectName("media_toolbar_btn")
        self.btn_play.setObjectName("media_toolbar_play")
        self.btn_prev.setObjectName("media_toolbar_prev")
        self.setObjectName("MediaToolBar")

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(self.slider)

        lower_layout = QHBoxLayout()
        lower_layout.insertWidget(0, self.btn_prev)
        lower_layout.insertWidget(1, self.btn_play)
        lower_layout.insertWidget(2, self.btn_next)

        lower_layout.insertWidget(3, self.music_label)
        lower_layout.insertWidget(4 ,QLabel("Volume"))
        lower_layout.insertWidget(5 ,self.slider_volume)
        lower_layout.insertWidget(6 ,self.btn_shuffle)
        lower_layout.insertWidget(7 ,self.btn_repeat)

        layout.addLayout(lower_layout)
        self.addWidget(container)

        if controller is not None:
            controller.set_song_slider(self.slider)
            controller.set_play_button(self.btn_play)
            controller.set_music_label(self.music_label)
            self.btn_play.clicked.connect(controller.toggle_play)
            self.btn_next.clicked.connect(controller.next_song)
            self.btn_prev.clicked.connect(controller.prev_song)
            
            self.btn_repeat.clicked.connect(lambda checked: controller.set_repeat(checked))
            self.btn_shuffle.clicked.connect(lambda checked: controller.toggle_shuffle(checked))

            self.slider.valueChanged.connect(lambda: controller.seek_by_percent(self.slider.value() / self.slider.maximum()))
            self.slider_volume.valueChanged.connect(controller.set_volume)



