import numpy as np
import pandas as pd
import pyqtgraph as pg
import scipy
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QWidget, QPushButton, QVBoxLayout, QSlider, QComboBox, QLabel, \
    QFormLayout, QTableWidget, QTableWidgetItem, QHeaderView, QFileDialog, QMessageBox , QGroupBox
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

        # First Section: Upload Button in a grey square
        upload_box = QGroupBox()
        upload_box.setStyleSheet("background-color: #d3d3d3; padding: 20px;")
        upload_layout = QVBoxLayout()
        upload_button = QPushButton("Upload")
        upload_button.setIcon(QIcon(
            "E:/cufe/biomedical department/3rd year/First Term/DSP/Task2/Signal-Studio/Icons/file-upload-icon.webp"))
        upload_button.setStyleSheet("font-size: 14px; padding: 10px;")
        upload_layout.addWidget(upload_button)
        upload_box.setLayout(upload_layout)
        toolbar_layout.addWidget(upload_box)
        upload_button.clicked.connect(self.upload_signal)


        # Add stretch to ensure equal spacing after the button
        toolbar_layout.addStretch(1)


        #second section
        table_box = QGroupBox("Signal Info")  # Set the title
        table_box.setStyleSheet("background-color: #d3d3d3; padding: 20px; font-size: 16px; font-weight: bold;")
        table_layout = QVBoxLayout()

        # Configure the table widget
        signal_info_table = QTableWidget()
        signal_info_table.setColumnCount(3)
        signal_info_table.setHorizontalHeaderLabels(["Name", "Frequency", "Amplitude"])
        signal_info_table.setEditTriggers(QTableWidget.NoEditTriggers)

        # Increase table size
        signal_info_table.setMinimumHeight(300)
        signal_info_table.setMaximumHeight(400)

        # Style the header and ensure it appears
        header = signal_info_table.horizontalHeader()
        header.setFont(QFont("Arial", 14, QFont.Bold))
        header.setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        header.setSectionResizeMode(QHeaderView.Stretch)  # Adjust to stretch headers
        header.setVisible(True)  # Ensure header visibility
        header = signal_info_table.horizontalHeader()
        header.setStyleSheet("""
                    QHeaderView::section {
                        padding: 8px;
                        background-color: #e0e0e0;
                        color: #333333;
                        font-size: 14px;
                        border: 1px solid #cccccc;
                    }
                """)

        # Set minimum height for the header
        header.setMinimumHeight(80)
        # Adjust row height and add data
        signal_info_table.verticalHeader().setDefaultSectionSize(35)  # Set row height
        signal_info_table.setWordWrap(False)  # Ensure text doesn't wrap in cells

        #pavly upload signal to table here
        signal_info_table.insertRow(0)
        signal_info_table.setItem(0, 0, QTableWidgetItem("Signal 1"))
        signal_info_table.setItem(0, 1, QTableWidgetItem("2 Hz"))
        signal_info_table.setItem(0, 2, QTableWidgetItem("3"))

        signal_info_table.insertRow(1)
        signal_info_table.setItem(1, 0, QTableWidgetItem("Signal 2"))
        signal_info_table.setItem(1, 1, QTableWidgetItem("5 Hz"))
        signal_info_table.setItem(1, 2, QTableWidgetItem("10"))

        # Center-align the cell content
        for row in range(signal_info_table.rowCount()):
            for col in range(signal_info_table.columnCount()):
                signal_info_table.item(row, col).setTextAlignment(Qt.AlignCenter)

        table_layout.addWidget(signal_info_table)
        table_box.setLayout(table_layout)
        table_box.setMinimumHeight(400)  # Increase section height
        toolbar_layout.addWidget(table_box)

        # Third Section: Sliders and Dropdowns in a smaller grey square
        controls_box = QGroupBox("Control Unit")  # Set the title
        controls_box.setStyleSheet("background-color: #d3d3d3; padding: 20px; font-size: 16px; font-weight: bold;")
        controls_layout = QVBoxLayout()
        controls_box.setMinimumHeight(200)  # Reduce height of this section

        # Slider function with increased label height
        def create_slider(label_text, default_value):
            slider_layout = QVBoxLayout()
            slider_label = QLabel(label_text)
            slider_label.setFixedHeight(25)  # Increased label height for readability
            slider = QSlider(Qt.Horizontal)
            slider.setRange(0, 100)
            slider.setValue(default_value)
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
            value_label = QLabel(f"{default_value}")
            value_label.setFixedHeight(25)  # Increased value label height for readability
            value_label.setAlignment(Qt.AlignCenter)
            slider.valueChanged.connect(lambda value: value_label.setText(f"{value}"))
            slider_layout.addWidget(slider_label)
            slider_layout.addWidget(slider)
            slider_layout.addWidget(value_label)
            return slider , slider_layout

        self.frequency_slider, frequency_slider_layout = create_slider("Sampling Frequency", 0)
        controls_layout.addLayout(frequency_slider_layout)
        self.frequency_slider.valueChanged.connect(self.update_stem_plot)

        self.SNR_slider, SNR_slider_layout = create_slider('SNR', 0)
        controls_layout.addLayout(SNR_slider_layout)
        self.SNR_slider.valueChanged.connect(lambda: self.update_plot_with_noise())

        # Dropdowns with increased padding and height
        dropdown_layout = QFormLayout()
        dropdown_layout.setSpacing(10)
        self.method_dropdown = QComboBox()
        self.method_dropdown.addItems(["Method1", "Method2", "Method3"])
        self.method_dropdown.setStyleSheet("padding: 5px; height: 30px;")  # Increase padding and height

        self.type_dropdown = QComboBox()
        self.type_dropdown.addItems(["Linear", "Sinusoid"])
        self.type_dropdown.setStyleSheet("padding: 5px; height: 30px;")  # Increase padding and height

        # Add space above each ComboBox label to prevent label cutoff
        method_label = QLabel("Select Method")
        method_label.setFixedHeight(30)  # Increased label height for visibility
        dropdown_layout.addRow(method_label, self.method_dropdown)

        reconstruction_label = QLabel("Reconstruction Method")
        reconstruction_label.setFixedHeight(30)  # Increased label height for visibility
        dropdown_layout.addRow(reconstruction_label, self.type_dropdown)

        controls_layout.addLayout(dropdown_layout)

        controls_box.setLayout(controls_layout)
        toolbar_layout.addWidget(controls_box)

        # Add resizing behavior for consistent layout
        toolbar_widget = QWidget()
        toolbar_widget.setLayout(toolbar_layout)
        toolbar_widget.setStyleSheet("background-color: #ffffff; padding: 10px;")

        horizontal_layout.addWidget(toolbar_widget)

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
        #print(self.calculate_max_frequency(self.amplitude))
        print(self.sampling_frequency)
        self.take_samples(self.time, self.amplitude, self.sampling_frequency)
        self.stem_plot(self.samples, self.sampled_amplitude)
        self.reconstruct(self.samples, self.sampled_amplitude)

    '''
        def calculate_max_frequency(self, amplitude):
        # Use FFT to find the maximum frequency component
        spectrum = np.fft.fft(amplitude)
        freqs = np.fft.fftfreq(len(amplitude), d=(self.time[1] - self.time[0]))  # Assuming uniform sampling
        max_freq = np.abs(freqs[np.argmax(np.abs(spectrum))])
        return max_freq

    '''

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
