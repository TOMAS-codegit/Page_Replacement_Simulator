from PySide6.QtWidgets import QApplication  
from MainWindow import MainWindow
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create the main window
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())
