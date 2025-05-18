from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt

class FifoSimulator:
    # Initializes the FIFO simulator with the UI object.
    def __init__(self, ui):
        self.ui = ui
        self.reference_string = []
        self.frames = []
        self.max_frames = 0
        self.current_index = 0
        self.page_faults = 0

    # Starts the FIFO simulation with the given reference string and number of frames.
    def start(self, reference_string, max_frames):
        self.reference_string = reference_string.split()
        self.max_frames = max_frames
        self.frames = []
        self.current_index = 0
        self.page_faults = 0
        self.ui.Hit_Miss_Line_Edit.setText("")
        self.ui.Page_Faults_Line_Edit.setText("")
        self.ui.Completion_Label.setVisible(False)
        self.clear_layouts()
        self.process_current_page()

    # Processes the next page in the reference string.
    def next(self):
        self.current_index += 1
        if self.current_index < len(self.reference_string):
            self.process_current_page()
        else:
            self.ui.Completion_Label.setVisible(True)

    # Processes the current page based on the FIFO algorithm.
    def process_current_page(self):
        self.clear_layouts()

        page = self.reference_string[self.current_index]

        # Determine HIT or MISS
        is_hit = page in self.frames
        if is_hit:
            self.ui.Hit_Miss_Line_Edit.setText("HIT")
        else:
            self.ui.Hit_Miss_Line_Edit.setText("MISS")
            self.page_faults += 1
            self.ui.Page_Faults_Line_Edit.setText(str(self.page_faults))

        # Current_Process view
        for i, p in enumerate(self.frames):
            if not is_hit and len(self.frames) >= self.max_frames and i == len(self.frames) - 1:
                self.add_box_to_frame(self.ui.Current_Process, p, "#D32F2F")  # remove color
            elif is_hit and p == page:
                self.add_box_to_frame(self.ui.Current_Process, p, "#4CAF50")  # hit color
            else:
                self.add_box_to_frame(self.ui.Current_Process, p)

        # Added_Page view
        self.add_box_to_frame(self.ui.Added_Page, page)

        # FIFO logic
        page_added = False
        if not is_hit:
            if len(self.frames) >= self.max_frames:
                self.frames.pop(0)  # Remove the oldest
            self.frames.append(page)
            page_added = True

        # New_Process view 
        for p in self.frames:
            if page_added and p == page:
                self.add_box_to_frame(self.ui.New_Process, p, "#2196F3")  # new page color
            elif is_hit and p == page:
                self.add_box_to_frame(self.ui.New_Process, p, "#4CAF50")  # hit color
            else:
                self.add_box_to_frame(self.ui.New_Process, p)

    # Clears the layouts of the current process, added page, and new process frames.
    def clear_layouts(self):
        self.clear_frame(self.ui.Current_Process)
        self.clear_frame(self.ui.Added_Page)
        self.clear_frame(self.ui.New_Process)

    # Clears all widgets from the given frame.
    def clear_frame(self, frame):
        layout = frame.layout()
        if layout:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.setParent(None)

    # Adds the frame on the simulation screen with the given page and color.
    def add_box_to_frame(self, frame, text, color=None):
        label = QLabel(text)
        style = "border: 1px solid #555; border-radius: 5px; padding: 5px; font-size: 16px; color: white;"
        if color:
            style = f"background-color: {color}; " + style
        label.setStyleSheet(style)
        label.setAlignment(Qt.AlignCenter)
        layout = frame.layout()
        if layout:
            layout.addWidget(label)

    # Clears the simulation and resets the UI.
    def clear_simulation(self):
        self.reference_string = []
        self.frames = []
        self.max_frames = 0
        self.current_index = 0
        self.page_faults = 0

        self.clear_layouts()
        self.clear_frame(self.ui.Page_Sequence_Container)
        self.ui.Hit_Miss_Line_Edit.setText("")
        self.ui.Page_Faults_Line_Edit.setText("")
        self.ui.Reference_String_Line_Edit.setText("")
        self.ui.Length_Line_Edit.setText("")
        self.ui.Frame_Line_Edit.setText("")
        self.ui.Completion_Label.setVisible(False)
        self.ui.Algorithm_Line_Edit.setText("")
