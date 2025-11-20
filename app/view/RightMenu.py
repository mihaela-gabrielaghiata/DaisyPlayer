from PySide6.QtCore import QSize
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QVBoxLayout, QLabel, QPushButton

assets_path = 'app/assets'

class RightMenu(QVBoxLayout):
    def __init__(self):
        super().__init__()
        label1 = QLabel('Element 1 în dreapta')
        label2 = QLabel('Element 2 în dreapta')
        buton_dreapta = QPushButton('Buton dreapta')

        self.addWidget(label1)
        self.addWidget(label2)
        self.addWidget(buton_dreapta)
        self.addStretch()
