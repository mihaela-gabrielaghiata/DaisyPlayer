import sys
from PySide6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QLabel,
        QPushButton, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy,
        QToolBar
)
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import QSize

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('DaisyPlayer')
        self.resize(1300, 800)

        toolbar = QToolBar()
        toolbar.setIconSize(QSize(48, 48))
        self.addToolBar(toolbar)

        toolbar.addAction(QAction(QIcon("icon.png"), "", self))

        layout_left = QVBoxLayout()
        self.button = QPushButton("Merge")
        
        layout_left.addWidget(self.button)
        layout_left.addStretch()

        layout_main = QHBoxLayout()
        layout_main.addLayout(layout_left)
        layout_main.addItem(QSpacerItem(1000, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        central_widget = QWidget()
        central_widget.setLayout(layout_main)

        self.setCentralWidget(central_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
