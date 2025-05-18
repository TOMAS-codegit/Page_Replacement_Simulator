from PySide6.QtWidgets import QLabel, QHBoxLayout
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

def display_page_sequence(container_widget, reference_string):
    # Clear previous widgets
    if container_widget.layout() is None:
        layout = QHBoxLayout()
        container_widget.setLayout(layout)
    else:
        layout = container_widget.layout()
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)

    # Add each number in its own styled QLabel square
    for num in reference_string.split():
        label = QLabel(num)
        label.setFixedSize(40, 40)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("background-color: #2d2d2d; border: 1px solid #555; border-radius: 5px; color: white;")
        label.setFont(QFont("Segoe UI", 14))
        layout.addWidget(label)