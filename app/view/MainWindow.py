from PySide6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QLabel,
        QPushButton, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy,
        QToolBar
)
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import QSize, Qt

assets_path = 'app/assets'

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('DaisyPlayer')
        self.resize(1300, 800)


        # -------------------------------
        # TOP TOOLBAR
        # -------------------------------
        toolbar = QToolBar()
        toolbar.setIconSize(QSize(48, 48))
        self.addToolBar(toolbar)
        toolbar.setStyleSheet('background-color: #4C6FA5;')

        toolbar.addAction(QAction(QIcon(f'{assets_path}/icons/icon.png'), '', self))

        # -------------------------------
        # PLAYER TOOLBAR
        # -------------------------------
        media_toolbar = QToolBar()
        media_toolbar.setIconSize(QSize(48, 48))
        media_toolbar.setStyleSheet('background-color: #7FB0FF;')

        self.addToolBar(Qt.BottomToolBarArea, media_toolbar)

        action_prev = QAction(QIcon(f'{assets_path}/icons/back.png'), 'Previous', self)
        action_play = QAction(QIcon(f'{assets_path}/icons/play.png'), 'Play', self)
        action_pause = QAction(QIcon(f'{assets_path}/icons/pause.png'), 'Pause', self)
        action_next = QAction(QIcon(f'{assets_path}/icons/next.png'), 'Next', self)

        media_toolbar.addAction(action_prev)
        media_toolbar.addAction(action_play)
        media_toolbar.addAction(action_pause)
        media_toolbar.addAction(action_next)

        # -------------------------------
        # LEFT MENU
        # -------------------------------
        layout_left = QVBoxLayout()
        self.button = QPushButton('Merge')
        
        layout_left.addWidget(self.button)
        layout_left.addStretch()
        
        # -------------------------------
        # RIGHT MENU
        # -------------------------------
        layout_right = QVBoxLayout()

        label1 = QLabel('Element 1 în dreapta')
        label2 = QLabel('Element 2 în dreapta')
        buton_dreapta = QPushButton('Buton dreapta')

        layout_right.addWidget(label1)
        layout_right.addWidget(label2)
        layout_right.addWidget(buton_dreapta)
        layout_right.addStretch()

        # -------------------------------
        # MAIN MENU
        # -------------------------------
        layout_main = QHBoxLayout()
        layout_main.addLayout(layout_left, 1)
        layout_main.addLayout(layout_right, 4)

        central_widget = QWidget()
        central_widget.setStyleSheet('background-color: #E7F1FF;')

        central_widget.setLayout(layout_main)

        self.setCentralWidget(central_widget)



