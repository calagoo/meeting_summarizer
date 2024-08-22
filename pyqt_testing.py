import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the window title
        self.setWindowTitle("PyQt Button Example")

        # Set the window size
        self.setGeometry(100, 100, 300, 200)

        # Initialize the UI components
        self.init_ui()

    def init_ui(self):
        """Initializes the UI components."""
        # Create a button
        self.button = QPushButton("Click Me", self)
        self.button.setGeometry(100, 80, 100, 40)  # Set the button position and size

        # Connect the button click signal to the event handler
        self.button.clicked.connect(self.on_button_click)

    def on_button_click(self):
        """Handle the button click event."""
        self.setWindowTitle("Button Clicked!")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the window title
        self.setWindowTitle("PyQt Button Example")

        # Set the window size
        self.setGeometry(100, 100, 300, 200)

        # Initialize the UI components
        self.init_ui()

    def init_ui(self):
        """Initializes the UI components."""
        # Create a button
        self.button = QPushButton("Click Me", self)
        self.button.setGeometry(100, 80, 100, 40)  # Set the button position and size

        # Connect the button click signal to the event handler
        self.button.clicked.connect(self.on_button_click)

    def on_button_click(self):
        """Handle the button click event."""
        self.setWindowTitle("Button Clicked!")
