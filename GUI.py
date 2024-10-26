import numpy as np
import pandas as pd
import pyqtgraph as pg
import scipy
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QWidget, QPushButton, QVBoxLayout, QSlider, QComboBox, QLabel, \
    QFormLayout, QTableWidget, QTableWidgetItem, QHeaderView, QFileDialog, QMessageBox
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

        self.data = []
        self.time = []
        self.amplitude = []
        self.sampled_amplitude = []
        self.sampling_frequency = 1

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
            "C:/Users/DELL/PycharmProjects/pythonProject1/New folder/file-upload-icon.webp"))
        upload_button.setStyleSheet("font-size: 14px; padding: 10px;")
        upload_button.clicked.connect(self.upload_signal)
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
            slider.setRange(1, 40)  # Set range (0 to 100)
            slider.setValue(0)  # Set default value
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

            return slider,slider_layout

        # Create and add the Sampling Frequency slider
        self.frequency_slider,slider_layout = create_slider("Sampling Frequency", 50)
        self.frequency_slider.valueChanged.connect(self.update_stem_plot)
        toolbar_layout.addLayout(slider_layout)

        # Add a stretch after the first slider layout
        toolbar_layout.addStretch(1)

        # Create and add the SNR slider
        self.SNR_slider , SNR_slider_layout = create_slider('SNR',50)
        toolbar_layout.addLayout(SNR_slider_layout)

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

    def upload_signal(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)",
                                                   options=options)
        if file_path:
            try:
                self.data = pd.read_csv(file_path)
                self.start()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load CSV file:\n{e}")

    def start(self):
        self.time = self.data.iloc[:, 0]
        self.amplitude = self.data.iloc[:, 1]
        self.take_samples(self.time, self.amplitude, self.sampling_frequency)
        self.stem_plot(self.samples, self.sampled_amplitude)
        self.plot(self.time, self.amplitude)
        self.reconstruct(self.samples, self.sampled_amplitude)

    def plot(self, time, amplitude):
        # Plot the original signal if not already plotted
        if not hasattr(self, 'original_plot') or self.original_plot is None:
            self.original_plot = self.signal_viewer.plot(time, amplitude, pen='b')
        else:
            self.original_plot.setData(time, amplitude)  # Update data if plot already exists

    def stem_plot(self, time, amplitude):
        # Clear previous sampled plots, including vertical lines and dots
        if hasattr(self, 'sampled_items'):
            for item in self.sampled_items:
                self.signal_viewer.removeItem(item)

        # Create a list to store the new sampled plot items (vertical lines and dots)
        self.sampled_items = []

        # Plot vertical lines and sample dots for the sampled signal
        for x, y in zip(time, amplitude):
            # Plot and store each vertical line
            line = self.signal_viewer.plot([x, x], [0, y], pen=pg.mkPen('w'))
            self.sampled_items.append(line)

        # Plot and store dots as a single item
        dots = self.signal_viewer.plot(time, amplitude, pen=None, symbol='o', symbolBrush='w')
        self.sampled_items.append(dots)

    def update_stem_plot(self):
        self.sampling_frequency = self.frequency_slider.value()
        print(self.calculate_max_frequency(self.amplitude))
        print(self.sampling_frequency)
        self.take_samples(self.time, self.amplitude, self.sampling_frequency)
        self.stem_plot(self.samples, self.sampled_amplitude)
        self.reconstruct(self.samples, self.sampled_amplitude)

    def calculate_max_frequency(self, amplitude):
        # Use FFT to find the maximum frequency component
        spectrum = np.fft.fft(amplitude)
        freqs = np.fft.fftfreq(len(amplitude), d=(self.time[1] - self.time[0]))  # Assuming uniform sampling
        max_freq = np.abs(freqs[np.argmax(np.abs(spectrum))])
        return max_freq

    def take_samples(self, time, amplitude, sampling_frequency):
        self.samples = np.arange(time[0], time[len(time) - 1], (1 / sampling_frequency))
        self.sampled_amplitude = np.interp(self.samples, time, amplitude)
        self.plot(self.time, self.amplitude)

    def reconstruct(self, samples, sampled_amplitude):
        self.reconstruction_viewer.clear()
        reconstructed_amplitude, reconstructed_time = scipy.signal.resample(sampled_amplitude, 5000, samples)
        self.reconstruction_viewer.plot(reconstructed_time, reconstructed_amplitude, pen='b')

    def get_difference_plot(self, plot1, plot2):
        pass

    def plot_frequency(self, frequency_plot):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = GUI()
    main_window.show()
    sys.exit(app.exec_())
