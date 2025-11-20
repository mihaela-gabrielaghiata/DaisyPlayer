from PySide6.QtWidgets import QVBoxLayout, QPushButton

assets_path = 'app/assets'

class LeftMenu(QVBoxLayout):
    def __init__(self):
        super().__init__()
        button = QPushButton('Merge')

        self.addWidget(button)
        self.addStretch()





