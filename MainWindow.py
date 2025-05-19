import os
import sys
import random
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtWidgets import QMainWindow, QMessageBox
from PySide6.QtUiTools import QUiLoader
from PageSequenceDisplay import display_page_sequence
from FifoSimulator import FifoSimulator
from LruSimulator import LruSimulator
from OptimalSimulator import OptimalSimulator

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Load the UI file correctly whether running normally or from a PyInstaller bundle
        loader = QUiLoader()
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS  # PyInstaller temporary folder
        else:
            base_path = os.path.abspath(".")

        ui_file_path = os.path.join(base_path, "Page_Simulator.ui")
        self.ui = loader.load(ui_file_path, None)

        # Hide completion label initially
        self.ui.Completion_Label.setVisible(False)

        # Disable buttons initially
        self.ui.Next_Button.setEnabled(False)
        self.ui.Start_Button.setEnabled(False)

        # Make certain fields read-only
        self.ui.Reference_String_Line_Edit.setReadOnly(True)
        self.ui.Hit_Miss_Line_Edit.setReadOnly(True)
        self.ui.Page_Faults_Line_Edit.setReadOnly(True)

        # Set up simulators
        self.fifo_simulator = FifoSimulator(self.ui)
        self.lru_simulator = LruSimulator(self.ui)
        self.optimal_simulator = OptimalSimulator(self.ui)

        # Algorithm selection
        self.selected_algorithm = None
        self.ui.FIFO_Button.clicked.connect(lambda: self.select_algorithm("FIFO"))
        self.ui.LRU_Button.clicked.connect(lambda: self.select_algorithm("LRU"))
        self.ui.Optimal_Button.clicked.connect(lambda: self.select_algorithm("OPTIMAL"))

        # Main button actions
        self.ui.Generate_Button.clicked.connect(self.generate_reference_string)
        self.ui.Confirm_Button.clicked.connect(self.on_confirm_clicked)
        self.ui.Clear_Button.clicked.connect(self.clear_simulation)
        self.ui.Start_Button.clicked.connect(self.start_simulation)
        self.ui.Next_Button.clicked.connect(self.next_step)

        # Window settings
        self.setWindowTitle("Page Replacement Algorithms")
        self.setMinimumSize(1000, 800)  # reasonable default
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setCentralWidget(self.ui)

    # Generate a random reference string based on user input and display it in the reference string line edit
    def generate_reference_string(self):
        length_text = self.ui.Length_Line_Edit.text()
        if not length_text.isdigit():
            QMessageBox.warning(self, "Invalid Input", "Length must be a number.")
            return

        length = int(length_text)
        if length > 12:
            QMessageBox.warning(self, "Limit Exceeded", "Maximum length allowed is 12.")
            return

        ref_string = [str(random.randint(0, 9)) for _ in range(length)]
        self.ui.Reference_String_Line_Edit.setText(" ".join(ref_string))

    # Display the page sequence in the container when the confirm button is clicked
    def on_confirm_clicked(self):
        reference = self.ui.Reference_String_Line_Edit.text()
        display_page_sequence(self.ui.Page_Sequence_Container, reference)
        self.ui.Start_Button.setEnabled(True)

    # Select the algorithm based on the button clicked
    def select_algorithm(self, algo):
        print(f"Selected algorithm: {algo}")
        self.selected_algorithm = algo

        # Set the Algorithm name in the Line Edit
        if self.selected_algorithm:
            self.ui.Algorithm_Line_Edit.setText(self.selected_algorithm)
        else:
            self.ui.Algorithm_Line_Edit.setText("None")
            return

    # Start the simulation
    def start_simulation(self):
        self.ui.Next_Button.setEnabled(True)
        reference = self.ui.Reference_String_Line_Edit.text()
        frame_text = self.ui.Frame_Line_Edit.text()

        if not reference or not frame_text.isdigit():
            print("Invalid reference or frame input")
            return

        frames = int(frame_text)

        if self.selected_algorithm == "FIFO":
            self.fifo_simulator.start(reference, frames)
        elif self.selected_algorithm == "LRU":
            self.lru_simulator.start(reference, frames)
        elif self.selected_algorithm == "OPTIMAL":
            self.optimal_simulator.start(reference, frames)

    # Display the next step in the simulation when the next button is clicked
    def next_step(self):
        if self.selected_algorithm == "FIFO":
            self.fifo_simulator.next()
        elif self.selected_algorithm == "LRU":
            self.lru_simulator.next()
        elif self.selected_algorithm == "OPTIMAL":
            self.optimal_simulator.next()

    # Clear the simulation and reset the UI
    def clear_simulation(self):
        self.fifo_simulator.clear_simulation()
        self.lru_simulator.clear_simulation()
        self.optimal_simulator.clear_simulation()
