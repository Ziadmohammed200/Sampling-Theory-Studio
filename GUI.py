import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QWidget, QPushButton, QVBoxLayout, QSlider, QComboBox, QLabel, \
    QFormLayout, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont
import sys


class GUI(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the main window properties
        self.setWindowTitle('Signal-Studio')
        self.resize(1400, 900)  # Set window size

        # Create a horizontal layout and set it as the main layout
        horizontal_layout = QHBoxLayout()
        horizontal_layout.setContentsMargins(0, 0, 0, 0)

        # Create the GraphicsLayoutWidget and set minimum size
        self.window = pg.GraphicsLayoutWidget(show=True, title="Signal Studio")
        self.window.resize(1200, 900)
        self.window.setMinimumSize(500, 500)
        self.window.setBackground('k')  # Set background color for the entire window

        # Create plots
        self.signal_viewer = self.window.addPlot(title="Signal Viewer")
        self.signal_viewer.setLabel('left', 'Amplitude')
        self.signal_viewer.setLabel('bottom', 'Time (s)')
        self.signal_viewer.setAspectLocked(False)
        self.signal_viewer.showGrid(x=True, y=True, alpha=0.4)

        self.reconstruction_viewer = self.window.addPlot(title="Reconstruction Viewer")
        self.reconstruction_viewer.setLabel('left', 'Amplitude')
        self.reconstruction_viewer.setLabel('bottom', 'Time (s)')
        self.reconstruction_viewer.setAspectLocked(False)
        self.reconstruction_viewer.showGrid(x=True, y=True, alpha=0.4)
        self.reconstruction_viewer.addLegend()

        # Move to the next row
        self.window.nextRow()

        self.difference_viewer = self.window.addPlot(title="Difference Viewer")
        self.difference_viewer.setLabel('left', 'Amplitude')
        self.difference_viewer.setLabel('bottom', 'Time (s)')
        self.difference_viewer.setAspectLocked(False)
        self.difference_viewer.showGrid(x=True, y=True, alpha=0.4)

        self.freq_viewer = self.window.addPlot(title="Frequency Viewer")
        self.freq_viewer.setLabel('left', 'Magnitude')
        self.freq_viewer.setLabel('bottom', 'Frequency (Hz)')
        self.freq_viewer.setAspectLocked(False)
        self.freq_viewer.showGrid(x=True, y=True, alpha=0.4)

        horizontal_layout.addWidget(self.window)

        # Create a vertical layout for the toolbar
        # Create a vertical layout for the toolbar
        # Create a vertical layout for the toolbar
        toolbar_layout = QVBoxLayout()
        toolbar_layout.setContentsMargins(50, 50, 50, 50)

        # Create and add the upload button with an icon
        upload_button = QPushButton("Upload")
        upload_button.setIcon(QIcon(
            "E:/cufe/biomedical department/3rd year/First Term/DSP/Task2/Signal-Studio/Icons/file-upload-icon.webp"))
        upload_button.setStyleSheet("font-size: 14px; padding: 10px;")
        toolbar_layout.addWidget(upload_button)

        # Add stretch to ensure equal spacing after the button
        toolbar_layout.addStretch(1)

        # Create a table widget for signal information
        signal_info_table = QTableWidget()
        signal_info_table.setColumnCount(3)  # Set the number of columns to 3
        signal_info_table.setHorizontalHeaderLabels(["Name", "Frequency", "Amplitude"])
        signal_info_table.setEditTriggers(QTableWidget.NoEditTriggers)  # Make the table read-only
        signal_info_table.horizontalHeader().setDefaultSectionSize(150)  # Set header width
        signal_info_table.horizontalHeader().setFont(QFont("Arial", 14, QFont.Bold))  # Set header font size
        signal_info_table.verticalHeader().setDefaultSectionSize(30)  # Set header height

        # Adjust column widths to fit content
        signal_info_table.resizeColumnsToContents()
        signal_info_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)  # Stretch the table to fill the layout

        # Set initial table data
        signal_info_table.insertRow(0)
        signal_info_table.setItem(0, 0, QTableWidgetItem("Signal 1"))
        signal_info_table.setItem(0, 1, QTableWidgetItem("2 Hz"))
        signal_info_table.setItem(0, 2, QTableWidgetItem("3"))

        signal_info_table.insertRow(1)
        signal_info_table.setItem(1, 0, QTableWidgetItem("Signal 2"))
        signal_info_table.setItem(1, 1, QTableWidgetItem("5 Hz"))
        signal_info_table.setItem(1, 2, QTableWidgetItem("10"))

        # Add the table to the toolbar layout
        toolbar_layout.addWidget(signal_info_table)

        # Function to create a slider with a value label
        def create_slider(label_text, default_value):
            # Create a vertical layout for the slider and label
            slider_layout = QVBoxLayout()

            # Create the slider
            slider = QSlider(Qt.Horizontal)
            slider.setRange(0, 100)  # Set range (0 to 100)
            slider.setValue(default_value)  # Set default value
            slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #999999;
                height: 8px;
                background: #f0f0f0;
                margin: 2px 0;
            }
            QSlider::handle:horizontal {
                background: #ffffff;
                border: 1px solid #5c5c5c;
                width: 18px;
                margin: -2px 0;
                border-radius: 3px;
            }
            QSlider::sub-page:horizontal {
                background: black;
                border: 1px solid #777;
                height: 8px;
                border-radius: 2px;
            }
            QSlider::add-page:horizontal {
                background: #f0f0f0;
                border: 1px solid #777;
                height: 8px;
                border-radius: 2px;
            }
            """)

            # Create a label for the slider value
            value_label = QLabel(f"{default_value}")
            value_label.setAlignment(Qt.AlignCenter)
            value_label.setStyleSheet("font-size: 12px; padding: 5px;")

            # Connect the slider's valueChanged signal to update the label
            slider.valueChanged.connect(lambda value: value_label.setText(f"{value}"))

            # Add the label and slider to the vertical layout
            slider_layout.addWidget(QLabel(label_text))  # Add label above the slider
            slider_layout.addWidget(slider)
            slider_layout.addWidget(value_label)

            return slider_layout

        # Create and add the Sampling Frequency slider
        toolbar_layout.addLayout(create_slider("Sampling Frequency", 50))

        # Add a stretch after the first slider layout
        toolbar_layout.addStretch(1)

        # Create and add the SNR slider
        toolbar_layout.addLayout(create_slider("SNR", 50))

        # Add a stretch after the second slider layout
        toolbar_layout.addStretch(1)

        # Create the dropdown list for methods
        self.method_dropdown = QComboBox()
        self.method_dropdown.addItems(["Method1", "Method2", "Method3"])
        self.method_dropdown.setStyleSheet("font-size: 12px; padding: 5px;")

        # Create the dropdown list for selecting the type
        self.type_dropdown = QComboBox()
        self.type_dropdown.addItems(["Linear", "Sinusoid"])  # Add options to the combobox
        self.type_dropdown.setStyleSheet("font-size: 12px; padding: 5px;")

        # Create a form layout for the dropdowns
        dropdown_layout = QFormLayout()

        method_label = QLabel("Select Method")
        method_label.setAlignment(Qt.AlignCenter)
        method_label.setStyleSheet("font-size: 12px; padding: 5px;")

        type_label = QLabel("Reconstruction Method")
        type_label.setAlignment(Qt.AlignCenter)
        type_label.setStyleSheet("font-size: 12px; padding: 5px;")

        # Add the labels and comboboxes to the form layout
        dropdown_layout.addRow(method_label, self.method_dropdown)
        dropdown_layout.addRow(type_label, self.type_dropdown)

        # Add the form layout to the toolbar layout
        toolbar_layout.addLayout(dropdown_layout)

        # Add a final stretch at the bottom for spacing
        toolbar_layout.addStretch(1)

        # Create a widget to contain the toolbar layout
        toolbar_widget = QWidget()
        toolbar_widget.setLayout(toolbar_layout)
        toolbar_widget.setStyleSheet("background-color: #f0f0f0; padding: 10px;")

        # Add the toolbar widget to the main horizontal layout
        horizontal_layout.addWidget(toolbar_widget)

        # Set the main layout for the window
        self.setLayout(horizontal_layout)

    def plot(self, time, amplitude):
        self.signal_viewer.clear()
        self.signal_viewer.plot(time, amplitude)

    def stem_plot(self):
        pass  # Implement functionality as needed

    def update_plot(self):
        pass  # Implement functionality as needed

    def get_difference_plot(self, plot1, plot2):
        pass  # Implement functionality as needed

    def plot_frequency(self, frequency_plot):
        pass  # Implement functionality as needed


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = GUI()
    main_window.show()
    sys.exit(app.exec_())
