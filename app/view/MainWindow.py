from PySide6.QtWidgets import (
    QMainWindow, QWidget, QLabel,
        QPushButton, QVBoxLayout, QHBoxLayout
)
from PySide6.QtCore import Qt

from app.view.LeftMenu import LeftMenu
from app.view.MainApp import MainApp
from app.view.RightMenu import RightMenu
from app.view.TopToolbar import TopToolbar
from app.view.MediaToolbar import MediaToolbar

assets_path = 'app/assets'

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('DaisyPlayer')
        self.resize(1300, 800)

        with open('app/view/stiluri/stil.qss','r') as f :
            qss=f.read()

        self.setStyleSheet(qss)


        # -------------------------------
        # TOP TOOLBAR
        # -------------------------------
        toolbar = TopToolbar()
        self.addToolBar(toolbar)

        # -------------------------------
        # PLAYER TOOLBAR
        # -------------------------------
        media_toolbar = MediaToolbar()
        self.addToolBar(Qt.BottomToolBarArea, media_toolbar)

        # -------------------------------
        # MAIN MENU
        # -------------------------------
        layout_main = MainApp()

        central_widget = QWidget()

        central_widget.setLayout(layout_main)

        self.setCentralWidget(central_widget)

