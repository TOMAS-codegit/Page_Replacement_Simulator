from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt

class OptimalSimulator:
    # Initializes the Optimal simulator with the UI object.
    def __init__(self, ui):
        self.ui = ui
        self.reference_string = []
        self.frames = []
        self.max_frames = 0
        self.current_index = 0
        self.page_faults = 0

    # Starts the Optimal simulation with the given reference string and number of frames.
    def start(self, reference_string, max_frames):
        self.reference_string = reference_string.split()
        self.max_frames = max_frames
        self.frames = []
        self.current_index = 0
        self.page_faults = 0
        self.ui.Hit_Miss_Line_Edit.setText("")
        self.ui.Page_Faults_Line_Edit.setText("")

        self.clear_layouts()
        self.ui.Completion_Label.setVisible(False)
        self.process_current_page()

    # Processes the next page in the reference string.
    def next(self):
        self.current_index += 1
        if self.current_index < len(self.reference_string):
            self.process_current_page()
        else:
            self.ui.Completion_Label.setVisible(True)

    # Processes the current page based on the Optimal algorithm.
    def process_current_page(self):
        self.clear_layouts()
        page = self.reference_string[self.current_index]

        # Prepare variables
        page_added = False
        to_replace = None
        old_frames = self.frames.copy()  # Preserve the original frame state for display

        # Optimal replacement logic
        if page not in self.frames:
            self.page_faults += 1
            page_added = True
            if len(self.frames) < self.max_frames:
                self.frames.append(page)
            else:
                to_replace = self.get_optimal_replacement()
                replace_index = self.frames.index(to_replace)
                self.frames[replace_index] = page

        # Display Current Frame state (before replacement)
        for f in old_frames:
            if to_replace and f == to_replace and page_added:
                self.add_box_to_frame(self.ui.Current_Process, f, "#D32F2F")  # Red = Removed
            elif f == page and not page_added:
                self.add_box_to_frame(self.ui.Current_Process, f, "#4CAF50")  # Green = Retained (hit)
            else:
                self.add_box_to_frame(self.ui.Current_Process, f)

        # Display Added Page
        self.add_box_to_frame(self.ui.Added_Page, page)

        # Update status fields
        self.ui.Hit_Miss_Line_Edit.setText("MISS" if page_added else "HIT")
        self.ui.Page_Faults_Line_Edit.setText(str(self.page_faults))

        # Display New Frame state (after replacement)
        for f in self.frames:
            if page_added and f == page:
                self.add_box_to_frame(self.ui.New_Process, f, "#2196F3")  # Blue = Added
            elif not page_added and f == page:
                self.add_box_to_frame(self.ui.New_Process, f, "#4CAF50")  # Green = Retained (hit)
            else:
                self.add_box_to_frame(self.ui.New_Process, f)

        # Completion check
        if self.current_index == len(self.reference_string) - 1:
            self.ui.Completion_Label.setVisible(True)

    # Determines the optimal page to replace based on future references.
    def get_optimal_replacement(self):
        future = self.reference_string[self.current_index + 1:]
        index_map = {f: (future.index(f) if f in future else float('inf')) for f in self.frames}
        return max(index_map, key=index_map.get)

    # Clears the layouts of the Current_Process, Added_Page, and New_Process frames.
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
