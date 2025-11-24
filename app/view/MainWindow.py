from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import (
    QMainWindow, QWidget
)
from PySide6.QtCore import Qt

from app.view.MainApp import MainApp
from app.view.TopToolbar import TopToolbar
from app.view.MediaToolbar import MediaToolbar
from app.controller.Controller import Controller

assets_path = 'app/assets'

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('DaisyPlayer')
        screen = QGuiApplication.primaryScreen().availableGeometry()
        width = screen.width()
        height = screen.height()
        self.resize(int(width * 0.85), int(height * 0.85))

        with open('app/view/stiluri/stil.qss','r') as f :
            qss=f.read()

        #self.setStyleSheet(qss)


        # -------------------------------
        # TOP TOOLBAR
        # -------------------------------
        toolbar = TopToolbar()
        self.addToolBar(toolbar)

        # -------------------------------
        # PLAYER TOOLBAR
        # -------------------------------
        controller = Controller.get_instance()
        media_toolbar = MediaToolbar(controller)
        self.addToolBar(Qt.BottomToolBarArea, media_toolbar)

        # -------------------------------
        # MAIN MENU
        # -------------------------------
        layout_main = MainApp()

        central_widget = QWidget()

        central_widget.setLayout(layout_main)

        self.setCentralWidget(central_widget)

