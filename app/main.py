import sys
from PySide6.QtWidgets import QApplication
from app.view.MainWindow import MainWindow

import os
os.environ["QT_DEBUG_PLUGINS"] = "1"
os.environ["QT_MEDIA_BACKEND"] = "ffmpeg"   # dacă ai ffmpeg


if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = MainWindow()
    with open("app/view/stiluri/stillDark.qss", "r") as f:
        app.setStyleSheet(f.read())


    window.show()

    sys.exit(app.exec())

